# Business Logic Security

**OWASP API Security Top 10 (2023): API10:2023 - Unsafe Consumption of APIs**

## The Problem

Business logic vulnerabilities occur when application workflows can be abused to perform unauthorized actions or bypass intended restrictions, even when all technical security controls (authentication, authorization, input validation) are correctly implemented.

**Key Difference:**
- **Technical Vulnerability**: Missing input validation, SQL injection
- **Business Logic Vulnerability**: Application works as coded, but workflow is flawed

## Why Critical

- **Cannot be detected by automated tools**: Logic flaws require understanding business rules
- **High business impact**: Direct financial loss, data manipulation, fraud
- **Difficult to fix**: Requires redesign of business processes

**CVSS Score**: Varies (7.0-9.0 depending on business impact)

---

## Common Business Logic Vulnerabilities

### 1. Race Conditions

**Problem:** Concurrent requests exploit timing windows

```python
# VULNERABLE - Race condition on account balance
@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    user = get_current_user()
    amount = request.json['amount']
    
    # Check balance (read)
    if user.balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # [RACE WINDOW HERE - Another request can execute]
    
    # Deduct balance (write)
    user.balance -= amount
    user.save()
    
    return jsonify({'success': True})

# Attack: Send 10 concurrent $100 withdrawal requests
# Balance: $100 → All 10 pass the balance check → Result: -$900 balance
```

**Secure Implementation:**

```python
# [APPROVED] SAFE - Atomic transaction with row locking
from sqlalchemy.orm import Session

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    user_id = get_current_user_id()
    amount = request.json['amount']
    
    session = Session()
    try:
        # Lock row for update (prevents concurrent modification)
        user = session.query(User).filter_by(id=user_id).with_for_update().first()
        
        # Check and update atomically
        if user.balance < amount:
            session.rollback()
            return jsonify({'error': 'Insufficient funds'}), 400
        
        user.balance -= amount
        session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
```

---

### 2. Negative Quantity Exploitation

**Problem:** Application accepts negative values where they don't make sense

```javascript
// VULNERABLE - No validation on quantity sign
app.post('/api/cart/add', (req, res) => {
  const { productId, quantity, price } = req.body;
  
  // Attacker sends quantity: -5
  // Result: Credits user account instead of charging
  const total = quantity * price;  // -5 * $100 = -$500 (refund)
  
  Cart.create({ productId, quantity, total });
});
```

**Secure Implementation:**

```javascript
// [APPROVED] SAFE - Validate business rules
app.post('/api/cart/add', (req, res) => {
  const { productId, quantity, price } = req.body;
  
  // Business rule validation
  if (quantity <= 0) {
    return res.status(400).json({ error: 'Quantity must be positive' });
  }
  
  if (quantity > 1000) {
    return res.status(400).json({ error: 'Quantity exceeds maximum' });
  }
  
  if (price < 0) {
    return res.status(400).json({ error: 'Invalid price' });
  }
  
  const total = quantity * price;
  Cart.create({ productId, quantity, total });
});
```

---

### 3. Price Manipulation

**Problem:** Client controls pricing

```javascript
// VULNERABLE - Client sends price
app.post('/api/checkout', async (req, res) => {
  const { productId, quantity, price } = req.body;
  
  // Attacker sends price: $0.01 for $1000 product
  const total = quantity * price;
  
  await Order.create({ productId, quantity, total });
});
```

**Secure Implementation:**

```javascript
// [APPROVED] SAFE - Server determines price
app.post('/api/checkout', async (req, res) => {
  const { productId, quantity } = req.body;
  
  // Fetch authoritative price from database
  const product = await Product.findById(productId);
  
  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }
  
  // Server calculates total (client cannot influence)
  const total = quantity * product.price;
  
  await Order.create({ productId, quantity, price: product.price, total });
});
```

---

### 4. Workflow Bypass

**Problem:** Steps can be skipped

```python
# VULNERABLE - No workflow state validation
@app.route('/api/orders/<id>/ship', methods=['POST'])
def ship_order(id):
    order = Order.query.get(id)
    order.status = 'shipped'
    order.save()
    
    # Attacker ships order before payment
```

**Secure Implementation:**

```python
# [APPROVED] SAFE - Enforce workflow state machine
class OrderStatus(enum.Enum):
    CREATED = 'created'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

ALLOWED_TRANSITIONS = {
    OrderStatus.CREATED: [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: []
}

@app.route('/api/orders/<id>/ship', methods=['POST'])
def ship_order(id):
    order = Order.query.get(id)
    
    # Validate current status
    if order.status != OrderStatus.PAID:
        return jsonify({
            'error': 'Order must be paid before shipping',
            'current_status': order.status.value
        }), 400
    
    # Validate state transition
    new_status = OrderStatus.SHIPPED
    if new_status not in ALLOWED_TRANSITIONS.get(order.status, []):
        return jsonify({'error': 'Invalid status transition'}), 400
    
    # Transition allowed
    order.status = new_status
    order.shipped_at = datetime.utcnow()
    order.save()
    
    return jsonify({'success': True})
```

---

### 5. Coupon/Discount Abuse

**Problem:** Coupons can be reused or combined

```python
# VULNERABLE - No coupon usage tracking
@app.route('/api/apply-coupon', methods=['POST'])
def apply_coupon():
    code = request.json['code']
    cart_id = request.json['cart_id']
    
    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon:
        return jsonify({'error': 'Invalid coupon'}), 400
    
    # Apply discount (can be used unlimited times)
    cart = Cart.query.get(cart_id)
    cart.discount += coupon.amount
    cart.save()
```

**Secure Implementation:**

```python
# [APPROVED] SAFE - Track coupon usage
@app.route('/api/apply-coupon', methods=['POST'])
def apply_coupon():
    code = request.json['code']
    cart_id = request.json['cart_id']
    user_id = get_current_user_id()
    
    coupon = Coupon.query.filter_by(code=code).first()
    
    if not coupon:
        return jsonify({'error': 'Invalid coupon'}), 400
    
    # Check if expired
    if coupon.expires_at < datetime.utcnow():
        return jsonify({'error': 'Coupon expired'}), 400
    
    # Check usage limit
    if coupon.usage_count >= coupon.max_uses:
        return jsonify({'error': 'Coupon usage limit reached'}), 400
    
    # Check if user already used this coupon
    previous_use = CouponUsage.query.filter_by(
        coupon_id=coupon.id,
        user_id=user_id
    ).first()
    
    if previous_use and not coupon.allow_multiple_uses:
        return jsonify({'error': 'Coupon already used'}), 400
    
    # Check if cart already has a coupon
    cart = Cart.query.get(cart_id)
    if cart.coupon_id and not coupon.stackable:
        return jsonify({'error': 'Cannot combine coupons'}), 400
    
    # Apply coupon
    cart.coupon_id = coupon.id
    cart.discount = coupon.amount
    cart.save()
    
    # Track usage
    CouponUsage.create(
        coupon_id=coupon.id,
        user_id=user_id,
        cart_id=cart_id,
        used_at=datetime.utcnow()
    )
    
    coupon.usage_count += 1
    coupon.save()
    
    return jsonify({'success': True})
```

---

### 6. Referral/Reward Fraud

**Problem:** Users create fake accounts to earn rewards

```python
# VULNERABLE - No fraud detection
@app.route('/api/referral/claim', methods=['POST'])
def claim_referral_reward():
    referrer_code = request.json['code']
    
    referrer = User.query.filter_by(referral_code=referrer_code).first()
    referrer.credits += 10  # $10 reward
    referrer.save()
    
    # Attacker creates 1000 fake accounts, earns $10,000
```

**Secure Implementation:**

```python
# [APPROVED] SAFE - Fraud detection
@app.route('/api/referral/claim', methods=['POST'])
def claim_referral_reward():
    referrer_code = request.json['code']
    new_user_id = get_current_user_id()
    
    referrer = User.query.filter_by(referral_code=referrer_code).first()
    new_user = User.query.get(new_user_id)
    
    # Cannot refer yourself
    if referrer.id == new_user_id:
        return jsonify({'error': 'Cannot refer yourself'}), 400
    
    # Check IP address fraud
    if referrer.last_login_ip == new_user.registration_ip:
        flag_potential_fraud(referrer.id, new_user_id, 'same_ip')
        return jsonify({'error': 'Invalid referral'}), 400
    
    # Check device fingerprint fraud
    if referrer.device_id == new_user.device_id:
        flag_potential_fraud(referrer.id, new_user_id, 'same_device')
        return jsonify({'error': 'Invalid referral'}), 400
    
    # Require new user to complete verification
    if not new_user.email_verified:
        return jsonify({'error': 'Email verification required'}), 400
    
    # Require new user to make first purchase before reward
    if not new_user.has_completed_purchase:
        return jsonify({'error': 'First purchase required'}), 400
    
    # Limit rewards per period
    recent_referrals = ReferralReward.query.filter(
        ReferralReward.referrer_id == referrer.id,
        ReferralReward.created_at > datetime.utcnow() - timedelta(days=7)
    ).count()
    
    if recent_referrals >= 10:
        return jsonify({'error': 'Weekly referral limit reached'}), 400
    
    # Grant reward
    referrer.credits += 10
    referrer.save()
    
    ReferralReward.create(
        referrer_id=referrer.id,
        referee_id=new_user_id,
        amount=10,
        created_at=datetime.utcnow()
    )
    
    return jsonify({'success': True})
```

---

## Testing Business Logic

**Security test cases:**

```python
def test_race_condition_prevention():
    """Test concurrent withdrawals don't overdraft"""
    user = create_test_user(balance=100)
    
    # Attempt 10 concurrent $50 withdrawals
    from concurrent.futures import ThreadPoolExecutor
    
    def withdraw():
        return client.post('/api/withdraw', 
                          json={'amount': 50},
                          headers={'Authorization': f'Bearer {user.token}'})
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: withdraw(), range(10)))
    
    # Only 2 should succeed (2 * $50 = $100)
    successful = sum(1 for r in results if r.status_code == 200)
    assert successful == 2
    
    # Final balance should be $0, not negative
    user.refresh()
    assert user.balance == 0

def test_negative_quantity_rejected():
    """Test negative quantities are rejected"""
    response = client.post('/api/cart/add', json={
        'product_id': 123,
        'quantity': -5  # Attempt negative quantity
    })
    
    assert response.status_code == 400
    assert 'positive' in response.json['error'].lower()

def test_workflow_enforcement():
    """Test order cannot be shipped before payment"""
    order = create_unpaid_order()
    
    response = client.post(f'/api/orders/{order.id}/ship')
    
    assert response.status_code == 400
    assert 'paid' in response.json['error'].lower()
```

---

## Verification Checklist

- [ ] Race conditions prevented with row locking/transactions
- [ ] Negative values rejected for quantities, prices, balances
- [ ] Server determines all authoritative values (price, tax, etc.)
- [ ] Workflow state machines enforce valid transitions
- [ ] Coupon/discount usage tracked and limited
- [ ] Referral fraud detection implemented
- [ ] Transaction limits on high-value operations
- [ ] Idempotency keys for critical operations
- [ ] Business rule validation on all inputs
- [ ] Automated tests for business logic edge cases

---

## References

- OWASP API Security Top 10 (2023): API10:2023
- OWASP Testing Guide: Business Logic Testing
- NIST SP 800-53: AC-3 (Access Enforcement)
