# Canon: User Guide Documentation

## Purpose

User guide documentation provides comprehensive instructions for end users to effectively use the product. It covers getting started, core features, workflows, troubleshooting, and FAQs, enabling users to accomplish tasks independently without support intervention.

---

## Scope

**This canon applies to:**
- End-user documentation for web applications, mobile apps, SaaS products
- Getting started guides
- Feature documentation
- Step-by-step tutorials
- Troubleshooting guides
- Frequently Asked Questions (FAQs)

**This canon does NOT apply to:**
- API documentation (use API documentation canons)
- Developer documentation (use separate developer guides)
- Internal admin documentation (use operations documentation)

---

## Access Level Classification

**User Guide Documentation:**
- **Access Level:** Public (Level 1)
- **Distribution:** End users, customers, general public
- **Storage:** Public documentation site (Read the Docs, GitHub Pages, etc.)
- **Review:** Product owner approval, technical writer review, UX review
- **Rationale:** Public-facing content for customer success

---

## When to Generate

### Initial Creation
- **Before Launch:** Create user guide before product release
- **Feature Complete:** When features are stable enough to document
- **Beta Release:** Minimal guide for beta testers

### Updates
- After new feature releases
- After UI/UX changes
- When user support tickets reveal documentation gaps
- Based on user feedback

### Frequency
- **Feature Releases:** Update with every feature launch
- **Regular Review:** Quarterly review for accuracy
- **User Feedback:** Monthly analysis of support tickets to identify gaps

---

## Files to Generate

Agent must create the following files when documenting user guides:

### 1. User Guide Index
**File:** `/docs/source/user-guide/00-index.rst`  
**Format:** reStructuredText  
**Purpose:** User guide entry point

### 2. Getting Started
**File:** `/docs/source/user-guide/01-getting-started.rst`  
**Format:** reStructuredText  
**Purpose:** Quick start guide, first steps for new users

### 3. Core Features
**Files:** `/docs/source/user-guide/features/*.rst`  
**Format:** reStructuredText  
**Purpose:** One file per major feature

### 4. Tutorials
**Files:** `/docs/source/user-guide/tutorials/*.rst`  
**Format:** reStructuredText  
**Purpose:** Step-by-step workflows for common tasks

### 5. Troubleshooting
**File:** `/docs/source/user-guide/troubleshooting.rst`  
**Format:** reStructuredText  
**Purpose:** Common issues and solutions

### 6. FAQ
**File:** `/docs/source/user-guide/faq.rst`  
**Format:** reStructuredText  
**Purpose:** Frequently Asked Questions

---

## Directory Structure

```
docs/source/user-guide/
├── 00-index.rst                    # User guide entry point
├── 01-getting-started.rst          # Quick start guide
├── features/
│   ├── tax-calculations.rst        # Tax calculation feature
│   ├── receipt-management.rst      # Receipt management feature
│   ├── user-profile.rst            # User profile feature
│   └── reporting.rst               # Reporting feature
├── tutorials/
│   ├── first-tax-calculation.rst   # Tutorial: First calculation
│   ├── generating-reports.rst      # Tutorial: Generate report
│   └── exporting-data.rst          # Tutorial: Export data
├── troubleshooting.rst             # Troubleshooting guide
└── faq.rst                         # Frequently Asked Questions
```

---

## Generation Rules

### User-Centric Language

Write for non-technical users:

**Do:**
- "Click the **Calculate** button"
- "Your tax amount appears below"
- "Enter your gross salary"

**Don't:**
- "Invoke the calculation API"
- "The server processes the request"
- "Submit POST data to /api/calculate"

### Task-Oriented Structure

Organize by what users want to accomplish:

**Good:**
- "How to calculate monthly taxes"
- "How to export receipts to PDF"
- "How to update your profile"

**Bad:**
- "Tax Calculation Service"
- "PDF Export Feature"
- "Profile Module"

### Screenshots and Visual Aids

Include screenshots for:
- UI navigation
- Complex workflows
- Form inputs
- Results interpretation

**Screenshot Guidelines:**
- Use clear, high-resolution images
- Highlight important UI elements (red boxes, arrows)
- Include captions explaining what the screenshot shows
- Update screenshots when UI changes

### Writing Style

Follow `00-core-canons/_core_canon.md` rules:
- No emojis, no emdashes
- Active voice ("Click the button" not "The button should be clicked")
- Simple, clear language
- Short paragraphs
- **Numbered lists for procedures**
- Avoid jargon or explain technical terms

---

## Content Guidelines

### User Guide Index (`/docs/source/user-guide/00-index.rst`)

```rst
User Guide
==========

Welcome to the Tax Management System user guide. This guide helps you calculate taxes,
manage receipts, and generate reports.

.. note::
   PUBLIC DOCUMENTATION - Level 1 Access
   This guide is publicly available to all users.

Getting Started
---------------

New to the Tax Management System? Start here:

- :doc:`01-getting-started` - Quick start guide (5 minutes)

Features
--------

Learn about core features:

.. toctree::
   :maxdepth: 1

   features/tax-calculations
   features/receipt-management
   features/user-profile
   features/reporting

Tutorials
---------

Step-by-step guides for common tasks:

.. toctree::
   :maxdepth: 1

   tutorials/first-tax-calculation
   tutorials/generating-reports
   tutorials/exporting-data

Need Help?
----------

- :doc:`troubleshooting` - Common issues and solutions
- :doc:`faq` - Frequently Asked Questions
- Contact Support: support@example.com

Quick Links
-----------

**Most Popular:**

- :ref:`calculating-taxes`
- :ref:`downloading-receipts`
- :ref:`exporting-pdf`
```

### Getting Started (`/docs/source/user-guide/01-getting-started.rst`)

```rst
Getting Started
===============

This quick start guide walks you through creating your first tax calculation in 5 minutes.

Step 1: Create an Account
--------------------------

1. Visit https://app.example.com
2. Click **Sign Up** in the top-right corner
3. Enter your email and create a password
4. Click **Create Account**
5. Check your email for verification link
6. Click the link to verify your account

.. figure:: images/signup-screen.png
   :alt: Sign up screen
   :width: 600px
   
   Sign up screen with email and password fields.

Step 2: Complete Your Profile
------------------------------

1. Log in with your credentials
2. Click your name in the top-right corner
3. Select **Profile** from the dropdown
4. Fill in your information:

   - Full Name
   - Phone Number
   - Country (select Kenya)
   
5. Click **Save Profile**

Step 3: Calculate Your First Tax
---------------------------------

1. From the dashboard, click **New Calculation**
2. Enter your gross monthly salary (e.g., 50,000)
3. Click **Calculate**
4. Your tax breakdown appears:

   - Gross Salary: KES 50,000
   - PAYE Tax: KES 5,250
   - Net Salary: KES 44,750

.. figure:: images/tax-calculation-result.png
   :alt: Tax calculation results
   :width: 700px
   
   Tax calculation results showing breakdown.

Step 4: Download Your Receipt
------------------------------

1. Click **Download Receipt** button
2. Choose format: **PDF** or **Excel**
3. Receipt downloads to your computer

Congratulations! You completed your first tax calculation.

Next Steps
----------

- :doc:`features/tax-calculations` - Learn advanced tax features
- :doc:`tutorials/generating-reports` - Create monthly reports
- :doc:`features/receipt-management` - Manage all your receipts
```

### Feature Documentation (`/docs/source/user-guide/features/tax-calculations.rst`)

```rst
.. _calculating-taxes:

Tax Calculations
================

Calculate Kenya Revenue Authority (KRA) compliant PAYE taxes.

Overview
--------

The tax calculation feature computes:

- Pay As You Earn (PAYE) tax
- National Hospital Insurance Fund (NHIF)
- National Social Security Fund (NSSF)
- Net salary after deductions

Supported Salary Ranges
------------------------

- Minimum: KES 1,000
- Maximum: KES 10,000,000
- Currency: Kenya Shillings (KES) only

How to Calculate Taxes
-----------------------

**Basic Calculation:**

1. Navigate to **Dashboard**
2. Click **New Calculation** button
3. Enter your **Gross Monthly Salary**
4. Click **Calculate**
5. Review your tax breakdown

**Advanced Calculation:**

1. Click **Advanced Options** (optional)
2. Enter additional allowances:

   - Housing Allowance
   - Transport Allowance
   - Medical Allowance
   
3. Enter deductions:

   - Pension Contributions
   - Life Insurance Premiums
   
4. Click **Calculate with Allowances**

Understanding Your Results
---------------------------

**Tax Breakdown:**

===============================  =================
Item                             Amount
===============================  =================
Gross Salary                     KES 50,000
PAYE Tax                         KES 5,250
NHIF Deduction                   KES 1,200
NSSF Deduction                   KES 1,080
-------------------------------  -----------------
**Net Salary**                   **KES 42,470**
===============================  =================

**Tax Rate:**

Your effective tax rate is shown as a percentage.

**Personal Relief:**

KRA personal relief (KES 2,400/month) is automatically applied.

Saving Calculations
-------------------

1. Complete a tax calculation
2. Click **Save Calculation**
3. Add optional notes
4. Click **Confirm**

Saved calculations appear in **My Calculations** history.

Exporting Results
-----------------

**Export to PDF:**

1. Complete a calculation
2. Click **Download PDF**
3. PDF includes:

   - Tax breakdown
   - Salary details
   - Calculation date
   - KRA compliance statement

**Export to Excel:**

1. Click **Download Excel**
2. Spreadsheet includes formulas for verification

Recalculating
-------------

To modify an existing calculation:

1. Go to **My Calculations**
2. Find the calculation
3. Click **Edit**
4. Update values
5. Click **Recalculate**

Troubleshooting
---------------

**Error: "Salary too high"**

Maximum salary is KES 10,000,000. Contact support for enterprise calculations.

**Error: "Invalid allowance amount"**

Allowances cannot exceed gross salary. Check your entries.

**Results seem incorrect**

Verify:

- Gross salary entered correctly
- Allowances in KES (not USD or other currency)
- Using current tax rates (2025)

See :doc:`../troubleshooting` for more help.
```

### Troubleshooting (`/docs/source/user-guide/troubleshooting.rst`)

```rst
Troubleshooting
===============

Common issues and solutions.

Login Issues
------------

**Cannot log in with correct password**

1. Check Caps Lock is off
2. Clear browser cache and cookies
3. Try password reset:

   a. Click **Forgot Password**
   b. Enter email
   c. Check email for reset link
   d. Create new password

**Account locked after multiple failed attempts**

Wait 30 minutes, then try again. Contact support if still locked.

Calculation Issues
------------------

**Tax calculation seems wrong**

Verify:

1. Gross salary entered correctly (no commas)
2. Using current tax year (2025)
3. Personal relief applied (should be KES 2,400)

Compare with KRA tax tables: https://kra.go.ke/tax-rates

**Cannot save calculation**

Check internet connection. Calculation saves require network connectivity.

Receipt Issues
--------------

**PDF download fails**

1. Disable browser popup blocker
2. Try different browser (Chrome, Firefox, Safari)
3. Check download folder permissions

**Receipt shows wrong date**

Receipts use calculation date, not download date. To update, recalculate with new date.

Browser Compatibility
---------------------

**Recommended Browsers:**

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Not Supported:**

- Internet Explorer (use Edge instead)
- Opera Mini

Contact Support
---------------

Still having issues?

**Email:** support@example.com  
**Response Time:** Within 24 hours  
**Include:**

- Description of problem
- Screenshot of error (if applicable)
- Browser and version
- Account email
```

---

## Validation

Agent must validate documentation before completion:

### reStructuredText Validation

```bash
# Validate all user guide reST files
rstcheck docs/source/user-guide/*.rst
rstcheck docs/source/user-guide/features/*.rst
rstcheck docs/source/user-guide/tutorials/*.rst
```

**Expected output:** No errors

### Screenshot Validation

- [ ] All screenshots up to date with current UI
- [ ] Screenshots clearly show referenced UI elements
- [ ] Captions explain what screenshot shows

### Sphinx Build Validation

```bash
# Build documentation with warnings as errors
sphinx-build -W -b html docs/source docs/build
```

**Expected output:** Build succeeds without warnings

---

## Examples Reference

See working example: `02-examples/user-guide-example/` (to be created)

**Example includes:**
- Complete user guide structure
- Getting started guide
- Feature documentation with screenshots
- Troubleshooting guide

---

## Access Level Note

User guides are typically Public (Level 1). Include at top:

```rst
.. note::
   PUBLIC DOCUMENTATION - Level 1 Access
   This guide is publicly available to all users.
```

---

## Agent Checklist

Before marking user guide documentation complete, verify:

- [ ] User guide index created
- [ ] Getting started guide with step-by-step instructions
- [ ] All major features documented
- [ ] Tutorials for common workflows included
- [ ] Troubleshooting guide with common issues
- [ ] FAQ included
- [ ] Screenshots current and clearly labeled
- [ ] User-centric language (no technical jargon)
- [ ] Task-oriented structure
- [ ] All links working
- [ ] Sphinx build succeeds without warnings
- [ ] No emojis or emdashes present

---

## Version History

**Version 1.0 - December 29, 2025**
- Initial user guide documentation canon
- Based on user-centered design principles
- Follows `_docs-canon.md` v4 specifications
