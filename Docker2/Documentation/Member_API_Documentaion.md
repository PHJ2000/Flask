# Member API Documentation

## Overview
This document describes the API endpoints for managing member data in our application.

## Base URL
`http://localhost:8000/member`

## Authentication
Describe your authentication mechanism here (e.g., Bearer Token, Basic Auth).

---

## Endpoints

### GET /member
Retrieve a list of members.

#### Parameters
- `searchType` (string): Filter by 'all', 'username', or 'name'.
- `searchText` (string): Search text to filter results.

#### Response
- `200 OK`: Successful retrieval of member list.
  - `pagination`: Object containing pagination data.
  - `items`: Array of member objects.

### POST /member
Create a new member.

#### Data
- `username` (string): Member's username (4-16 characters, must start with a letter and include a number).
- `password` (string): Member's password (8-16 characters).
- `passwordMatch` (string): Confirmation of the password.
- `name` (string): Member's name (2-10 characters in Korean).

#### Response
- `201 Created`: Successful creation of a new member.
  - `data`: Object containing the created member's data.

### GET /member/{member_idx}
Retrieve details for a specific member.

#### Parameters
- `member_idx` (integer): Unique identifier of the member.

#### Response
- `200 OK`: Successful retrieval of member details.
  - `data`: Object containing the member's details.
- `404 Not Found`: Member with the specified ID was not found.

### PUT /member/{member_idx}
Update details for a specific member.

#### Data
- `oldPassword` (string): Current password of the member.
- `newPassword` (string): New password for the member.
- `newPasswordMatch` (string): Confirmation of the new password.
- `name` (string): New name of the member.

#### Response
- `200 OK`: Successful update of member details.
  - `data`: Object containing the updated member's details.
- `404 Not Found`: Member with the specified ID was not found.

### DELETE /member/{member_idx}
Delete a specific member.

#### Parameters
- `member_idx` (integer): Unique identifier of the member to be deleted.

#### Response
- `200 OK`: Successful deletion of the member.
  - `message`: Success message.
- `404 Not Found`: Member with the specified ID was not found.

---

## Errors
Describe common error responses (e.g., `400 Bad Request`, `401 Unauthorized`, `500 Internal Server Error`).

## Notes
Add any additional information, assumptions, or constraints related to the API.
