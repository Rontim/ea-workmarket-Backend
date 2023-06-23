# EA Workmarket API Documentation

This documentation provides an overview of the API endpoints available in the EA Workmarket application.

## User Registration

- **POST /auth/users/**: Register a new user.

## User Authentication

- **POST /auth/jwt/create/**: Obtain an authentication token.
- **POST /auth/token/logout/**: Logout and invalidate the authentication token.
- **POST /auth/jwt/create/**: Refresh the authentication token.

## User Profile

- **GET /profile/ :** Retrieve a profile for read only or for authenticated user
- **POST /profile/create/ :** Creating a new profile
- **PUT /profile/update/ :** Update the full profile
- **PATCH /profile/update/ :** Update a specific field

## Job Listings

- **GET /jobs/**: Retrieve a list of all jobs.
- **POST /jobs/**: Create a new job listing.
- **GET /jobs/{job_id}/**: Retrieve a specific job by ID.
- **PUT /jobs/{job_id}/**: Update a specific job by ID.
- **DELETE /jobs/{job_id}/**: Delete a specific job by ID.
- **GET /account/bidder-profile/{username}/ :** Retrieve the profile of a bidder.

## Job Bids

- **GET /jobs/{job_id}/bids/**: Retrieve all bids for a specific job.
- **POST /jobs/{job_id}/bids/**: Create a new bid for a specific job.
- **GET /bids/{bid_id}/**: Retrieve a specific bid by ID.
- **PUT /bids/{bid_id}/**: Update a specific bid by ID.
- **DELETE /bids/{bid_id}/**: Delete a specific bid by ID.

## Payment Integration

- **POST /payments/initiate/**: Initiate a payment transaction.
- **POST /payments/callback/**: Handle the payment callback request.
