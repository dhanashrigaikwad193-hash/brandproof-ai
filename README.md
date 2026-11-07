# BrandProof AI

## Claim Passport — AI-Assisted Brand Claim Verification

BrandProof AI is a Flask-based claim verification assistant for small businesses and marketing teams.

It checks marketing claims against approved evidence and identifies whether each claim is:

- Supported
- Conflict
- Needs Verification

For conflicting numeric claims, the system also provides the evidence value and a suggested correction.

## Live Demo

https://brandproof-ai-1.onrender.com

## Problem

Marketing content can contain unsupported, outdated, or conflicting product claims.

BrandProof AI provides a simple way to compare marketing drafts with approved evidence before publishing.

## How It Works

1. Enter a marketing draft.
2. Enter approved product evidence.
3. Enter the evidence review date.
4. Click **Check Claims**.
5. Review the Claim Passport results.

Each detected claim receives a status and explanation.

## Current Features

- Marketing draft input
- Approved evidence input
- Claim-level verification
- Supported claim detection
- Numeric conflict detection
- Needs Verification detection
- Evidence used explanation
- Suggested correction for conflicting numeric claims
- Evidence Freshness review reminder
- Mobile-friendly Flask web interface

## Example

### Marketing Draft

> Our EcoBottle is made from recyclable materials.  
> Our EcoBottle lasts for 10 years.  
> Customers can save 40% with EcoBottle.

### Approved Evidence

> EcoBottle is made from recyclable materials.  
> The expected product life is approximately 5 years.

### Result

- Recyclable materials → Supported
- 10 years → Conflict
- 40% savings → Needs Verification

## Technology

- Python
- Flask
- HTML
- CSS
- Gunicorn
- Render
- GitHub

## Architecture

User Marketing Draft  
↓  
Claim Extraction  
↓  
Evidence Comparison  
↓  
Claim Status  
↓  
Explanation / Suggested Correction  
↓  
Claim Passport Result

## Current Limitations

The current MVP compares claims only against evidence supplied by the user.

Missing evidence does not automatically mean that a claim is false.

The current version uses rule-based matching rather than a large language model.

Human review is recommended before publishing important marketing claims.

## Round 3 Planned Improvements

1. Claim Passport Dashboard
2. Evidence Conflict & History
3. Exportable BrandProof Report

## Team

**Team:** TRUSTFORGE

**Project:** BrandProof AI

## Deployment

The application is deployed as a public Flask web service on Render.

Live URL:

https://brandproof-ai-1.onrender.com
