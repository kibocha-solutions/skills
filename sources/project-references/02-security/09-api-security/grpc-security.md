# gRPC Security

**OWASP API Security Top 10 (2023): Adapted for gRPC**

## The Problem

gRPC, while providing performance benefits through Protocol Buffers and HTTP/2, introduces unique security challenges including reflection attacks, lack of built-in authentication, TLS misconfiguration, and protobuf deserialization vulnerabilities.

## Why Critical

- **Binary Protocol**: Harder to inspect and monitor
- **High Performance**: Amplifies impact of attacks
- **Microservices**: Compromise spreads quickly across services
- **Complex Auth**: No standard authentication mechanism

**CVSS Score**: 7.0-9.0 (HIGH to CRITICAL)

---

## gRPC-Specific Vulnerabilities

### 1. gRPC Reflection Attacks

**Problem:** Server reflection exposes all service definitions

```bash
# Attacker uses grpcurl to discover services
grpcurl -plaintext localhost:50051 list

# Output reveals all services:
grpc.health.v1.Health
myservice.UserService
myservice.AdminService        # Internal service exposed
myservice.InternalDebugService  # Debug service in production

# Attacker lists methods
grpcurl -plaintext localhost:50051 list myservice.AdminService

# Output:
myservice.AdminService.ResetDatabase
myservice.AdminService.GetAllUserPasswords  # Critical vulnerability
```

**Secure Implementation:**

```go
// [APPROVED] Disable reflection in production
package main

import (
    "google.golang.org/grpc"
    "google.golang.org/grpc/reflection"
    "os"
)

func main() {
    server := grpc.NewServer()
    
    // Register services
    pb.RegisterUserServiceServer(server, &userService{})
    
    // Only enable reflection in development
    if os.Getenv("ENV") != "production" {
        reflection.Register(server)
    }
    
    server.Serve(listener)
}
```

```python
# [APPROVED] Python - disable reflection
import grpc
from grpc_reflection.v1alpha import reflection
import os

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Register services
user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

# Only enable reflection in development
if os.getenv('ENV') != 'production':
    SERVICE_NAMES = (
        user_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

server.add_insecure_port('[::]:50051')
server.start()
```

---

### 2. Missing/Weak Authentication

**Problem:** gRPC has no built-in authentication

```go
// VULNERABLE - No authentication
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    // Anyone can call this
    user := database.GetUser(req.UserId)
    return user, nil
}
```

**Secure Implementation:**

```go
// [APPROVED] Token-based authentication with metadata
package main

import (
    "context"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/metadata"
    "google.golang.org/grpc/status"
)

// Interceptor for authentication
func authInterceptor(
    ctx context.Context,
    req interface{},
    info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler,
) (interface{}, error) {
    // Extract metadata
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.Unauthenticated, "Missing metadata")
    }
    
    // Get authorization token
    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "Missing token")
    }
    
    token := tokens[0]
    
    // Verify token
    user, err := verifyJWT(token)
    if err != nil {
        return nil, status.Error(codes.Unauthenticated, "Invalid token")
    }
    
    // Add user to context
    ctx = context.WithValue(ctx, "user", user)
    
    // Call handler
    return handler(ctx, req)
}

func main() {
    server := grpc.NewServer(
        grpc.UnaryInterceptor(authInterceptor),  // Apply to all RPCs
    )
    
    pb.RegisterUserServiceServer(server, &userService{})
    server.Serve(listener)
}

// Service method with authorization
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    // Get authenticated user from context
    currentUser := ctx.Value("user").(*User)
    
    // Authorization check
    if currentUser.ID != req.UserId && !currentUser.IsAdmin {
        return nil, status.Error(codes.PermissionDenied, "Access denied")
    }
    
    user := database.GetUser(req.UserId)
    return user, nil
}
```

---

### 3. Insecure TLS Configuration

**Problem:** gRPC running without TLS or with weak TLS

```go
// VULNERABLE - No TLS (plaintext)
server := grpc.NewServer()
listener, _ := net.Listen("tcp", ":50051")
server.Serve(listener)  // Unencrypted traffic
```

**Secure Implementation:**

```go
// [APPROVED] TLS 1.3 with strong ciphers
package main

import (
    "crypto/tls"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"
)

func main() {
    // Load TLS certificate
    cert, err := tls.LoadX509KeyPair("server.crt", "server.key")
    if err != nil {
        log.Fatalf("Failed to load TLS cert: %v", err)
    }
    
    // TLS configuration
    tlsConfig := &tls.Config{
        Certificates: []tls.Certificate{cert},
        MinVersion:   tls.VersionTLS13,  // TLS 1.3 minimum
        CipherSuites: []uint16{
            tls.TLS_AES_128_GCM_SHA256,
            tls.TLS_AES_256_GCM_SHA384,
            tls.TLS_CHACHA20_POLY1305_SHA256,
        },
        ClientAuth: tls.RequireAndVerifyClientCert,  // mTLS
    }
    
    // Create credentials
    creds := credentials.NewTLS(tlsConfig)
    
    // Create server with TLS
    server := grpc.NewServer(grpc.Creds(creds))
    
    pb.RegisterUserServiceServer(server, &userService{})
    
    listener, _ := net.Listen("tcp", ":50051")
    server.Serve(listener)
}
```

---

### 4. Protobuf Deserialization Vulnerabilities

**Problem:** Malicious protobuf messages exploit parser

```protobuf
// Protobuf with nested messages
message User {
  string name = 1;
  repeated Post posts = 2;
}

message Post {
  string title = 1;
  repeated Comment comments = 2;
}

message Comment {
  string text = 1;
  User author = 2;  // Circular reference possible
}
```

```
// Attacker sends deeply nested message
User {
  posts: [
    Post {
      comments: [
        Comment {
          author: User {
            posts: [... nested 1000 levels]
          }
        }
      ]
    }
  ]
}

// Result: Stack overflow, DoS
```

**Secure Implementation:**

```go
// [APPROVED] Message size limits and validation
import (
    "google.golang.org/grpc"
)

func main() {
    server := grpc.NewServer(
        grpc.MaxRecvMsgSize(1 * 1024 * 1024),  // 1MB max message size
        grpc.MaxSendMsgSize(1 * 1024 * 1024),
        grpc.MaxConcurrentStreams(100),         // Limit concurrent streams
    )
    
    pb.RegisterUserServiceServer(server, &userService{})
    server.Serve(listener)
}

// Validate message depth
func (s *server) CreateUser(ctx context.Context, req *pb.User) (*pb.User, error) {
    // Validate request
    if err := validateUserMessage(req, 0, 5); err != nil {
        return nil, status.Error(codes.InvalidArgument, err.Error())
    }
    
    // Process request
    return s.db.CreateUser(req), nil
}

func validateUserMessage(user *pb.User, currentDepth, maxDepth int) error {
    if currentDepth > maxDepth {
        return fmt.Errorf("message depth exceeds limit of %d", maxDepth)
    }
    
    // Validate nested messages
    for _, post := range user.Posts {
        if err := validatePostMessage(post, currentDepth+1, maxDepth); err != nil {
            return err
        }
    }
    
    return nil
}
```

---

### 5. Missing Request Validation

**Problem:** No validation on protobuf messages

```protobuf
message CreateUserRequest {
  string username = 1;
  string email = 2;
  int32 age = 3;
}
```

```go
// VULNERABLE - No validation
func (s *server) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
    // Attacker sends:
    // username: "" (empty)
    // email: "not-an-email"
    // age: -100 (negative)
    
    user := &User{
        Username: req.Username,  // Empty string allowed
        Email: req.Email,        // Invalid email allowed
        Age: req.Age,            // Negative age allowed
    }
    return s.db.Create(user), nil
}
```

**Secure Implementation:**

```go
// [APPROVED] Request validation
import (
    "regexp"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

var emailRegex = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)

func (s *server) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
    // Validate username
    if len(req.Username) < 3 || len(req.Username) > 30 {
        return nil, status.Error(codes.InvalidArgument, "Username must be 3-30 characters")
    }
    
    // Validate email
    if !emailRegex.MatchString(req.Email) {
        return nil, status.Error(codes.InvalidArgument, "Invalid email format")
    }
    
    // Validate age
    if req.Age < 0 || req.Age > 150 {
        return nil, status.Error(codes.InvalidArgument, "Age must be between 0 and 150")
    }
    
    // Create user
    user := &User{
        Username: req.Username,
        Email: req.Email,
        Age: req.Age,
    }
    
    return s.db.Create(user), nil
}
```

---

### 6. Rate Limiting

**Problem:** No built-in rate limiting in gRPC

```go
// VULNERABLE - No rate limiting
func (s *server) SendEmail(ctx context.Context, req *pb.EmailRequest) (*pb.Empty, error) {
    sendEmail(req.To, req.Subject, req.Body)
    return &pb.Empty{}, nil
}

// Attacker sends 10,000 email requests
```

**Secure Implementation:**

```go
// [APPROVED] gRPC rate limiting interceptor
import (
    "golang.org/x/time/rate"
    "sync"
)

type rateLimiter struct {
    limiters map[string]*rate.Limiter
    mu       sync.RWMutex
}

func newRateLimiter() *rateLimiter {
    return &rateLimiter{
        limiters: make(map[string]*rate.Limiter),
    }
}

func (rl *rateLimiter) getLimiter(key string) *rate.Limiter {
    rl.mu.RLock()
    limiter, exists := rl.limiters[key]
    rl.mu.RUnlock()
    
    if !exists {
        rl.mu.Lock()
        limiter = rate.NewLimiter(10, 20)  // 10 req/sec, burst of 20
        rl.limiters[key] = limiter
        rl.mu.Unlock()
    }
    
    return limiter
}

func rateLimitInterceptor(rl *rateLimiter) grpc.UnaryServerInterceptor {
    return func(
        ctx context.Context,
        req interface{},
        info *grpc.UnaryServerInfo,
        handler grpc.UnaryHandler,
    ) (interface{}, error) {
        // Get client IP from context
        clientIP := getClientIP(ctx)
        
        // Check rate limit
        limiter := rl.getLimiter(clientIP)
        if !limiter.Allow() {
            return nil, status.Error(codes.ResourceExhausted, "Rate limit exceeded")
        }
        
        return handler(ctx, req)
    }
}

func main() {
    rl := newRateLimiter()
    
    server := grpc.NewServer(
        grpc.UnaryInterceptor(rateLimitInterceptor(rl)),
    )
    
    pb.RegisterEmailServiceServer(server, &emailService{})
    server.Serve(listener)
}
```

---

### 7. Stream Security

**Problem:** Bidirectional streams not properly secured

```go
// VULNERABLE - No stream limits
func (s *server) Chat(stream pb.ChatService_ChatServer) error {
    for {
        msg, err := stream.Recv()
        if err != nil {
            return err
        }
        
        // Process message (no limits on message count/size)
        stream.Send(&pb.ChatMessage{Text: "Echo: " + msg.Text})
    }
}
```

**Secure Implementation:**

```go
// [APPROVED] Stream with limits
import (
    "context"
    "time"
)

func (s *server) Chat(stream pb.ChatService_ChatServer) error {
    const (
        maxMessages = 1000
        maxDuration = 1 * time.Hour
        maxMessageSize = 1024  // 1KB
    )
    
    ctx, cancel := context.WithTimeout(stream.Context(), maxDuration)
    defer cancel()
    
    messageCount := 0
    
    for {
        select {
        case <-ctx.Done():
            return status.Error(codes.DeadlineExceeded, "Stream timeout")
        default:
        }
        
        // Receive message
        msg, err := stream.Recv()
        if err != nil {
            return err
        }
        
        // Check message count
        messageCount++
        if messageCount > maxMessages {
            return status.Error(codes.ResourceExhausted, "Message limit exceeded")
        }
        
        // Check message size
        if len(msg.Text) > maxMessageSize {
            return status.Error(codes.InvalidArgument, "Message too large")
        }
        
        // Process and send
        stream.Send(&pb.ChatMessage{Text: "Echo: " + msg.Text})
    }
}
```

---

## gRPC Security Checklist

- [ ] Reflection disabled in production
- [ ] TLS 1.3 configured with strong ciphers
- [ ] Mutual TLS (mTLS) for service-to-service
- [ ] Authentication interceptor on all services
- [ ] Authorization checks in each RPC method
- [ ] Message size limits configured (1MB max)
- [ ] Request validation implemented
- [ ] Rate limiting interceptor configured
- [ ] Stream limits enforced (count, size, duration)
- [ ] Error messages generic (no internal details)
- [ ] Logging and monitoring enabled
- [ ] Service mesh for additional security (Istio, Linkerd)

---

## Testing gRPC Security

```go
func TestGRPCAuthentication(t *testing.T) {
    // Attempt RPC without authentication
    conn, _ := grpc.Dial("localhost:50051", grpc.WithInsecure())
    client := pb.NewUserServiceClient(conn)
    
    _, err := client.GetUser(context.Background(), &pb.GetUserRequest{UserId: "123"})
    
    // Should fail without auth
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Unauthenticated")
}

func TestGRPCRateLimiting(t *testing.T) {
    conn, _ := grpc.Dial("localhost:50051", grpc.WithInsecure())
    client := pb.NewEmailServiceClient(conn)
    
    // Send 100 requests rapidly
    failures := 0
    for i := 0; i < 100; i++ {
        _, err := client.SendEmail(context.Background(), &pb.EmailRequest{
            To: "test@example.com",
            Subject: "Test",
            Body: "Test",
        })
        if err != nil {
            failures++
        }
    }
    
    // Some should be rate limited
    assert.Greater(t, failures, 0)
}
```

---

## References

- gRPC Security Guide
- gRPC Authentication Guide
- Protocol Buffers Security
- OWASP API Security Top 10 (2023)
- TLS Best Practices for gRPC
