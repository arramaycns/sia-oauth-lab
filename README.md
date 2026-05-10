# OAuth 2.0 Lab: Securing APIs with GitHub

**Course:** System Integration and Architecture  
**Laboratory Activity:** Securing APIs using OAuth 2.0 with GitHub

## Project Overview
This repository contains a Flask-based web application demonstrating how to secure APIs using the OAuth 2.0 authorization framework. It integrates with GitHub as the Identity Provider (IdP), allowing users to securely authenticate without exposing their passwords to this application. 

The user interface has been custom-designed using clean, modern iOS-style CSS to provide a native mobile-like experience in the browser.

## Features
* **GitHub OAuth Authentication:** Secure login using GitHub credentials.
* **Protected Routes:** Unauthorized users are blocked from accessing the `/profile` and API endpoints.
* **Dynamic Profile Dashboard:** Parses and cleanly displays GitHub API data (avatar, bio, followers, repos, etc.).
* **Session Management:** Secure login and logout functionality that properly creates and destroys user sessions.
* **Bonus Challenge Completed:** Includes a highly secure backend API endpoint (`/api/secure-data`) that verifies session tokens before returning JSON data.

## Technology Stack
* **Backend:** Python, Flask
* **Authentication:** OAuth 2.0, Authlib
* **Frontend:** HTML5, Embedded CSS (iOS Human Interface styling)
* **Identity Provider:** GitHub API

## How to Run the Application

### Prerequisites
1. Python 3 installed on your machine.
2. A GitHub account.
3. A registered GitHub OAuth Application (with `http://localhost:5000/callback` as the Authorization Callback URL).

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/sia-oauth-lab.git](https://github.com/YOUR_GITHUB_USERNAME/sia-oauth-lab.git)
   cd sia-oauth-lab