# Business Outreach Platform - Database Schema

This document details the database schema for the Business Outreach Platform, based on the data models defined in `api_spec.md`. We will use PostgreSQL as the relational database.

## 1. Table: `businesses`

Stores information about each business.

```sql
CREATE TABLE businesses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    website VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    address TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending_scan',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_businesses_name ON businesses (name);
CREATE INDEX idx_businesses_status ON businesses (status);
```

**Notes:**
*   `status` can be one of: `pending_scan`, `scanned`, `active`, `archived`.
*   `name` is unique to prevent duplicate business entries.

## 2. Table: `contacts`

Stores various contact methods found for each business.

```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    value TEXT NOT NULL,
    source VARCHAR(50) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (business_id, type, value) -- Prevent duplicate contacts for the same business and type
);

CREATE INDEX idx_contacts_business_id ON contacts (business_id);
CREATE INDEX idx_contacts_type ON contacts (type);
```

**Notes:**
*   `type` can be one of: `email`, `instagram`, `facebook`, `twitter`, `linkedin`, `phone`, `contact_form`.
*   `source` can be one of: `csv`, `scanned_website`, `scanned_social_media`.
*   `ON DELETE CASCADE` ensures that if a business is deleted, all its associated contacts are also deleted.

## 3. Table: `campaigns`

Stores information about each outreach campaign.

```sql
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    message_template TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_campaigns_name ON campaigns (name);
CREATE INDEX idx_campaigns_status ON campaigns (status);
```

**Notes:**
*   `status` can be one of: `draft`, `scheduled`, `sending`, `paused`, `completed`, `cancelled`.

## 4. Table: `messages`

Stores details for each individual message sent as part of a campaign.

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    business_id INTEGER NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    personalized_content TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    opened_at TIMESTAMP WITH TIME ZONE,
    replied_at TIMESTAMP WITH TIME ZONE,
    UNIQUE (campaign_id, business_id, contact_id, platform) -- Prevent duplicate messages for the same campaign, business, contact, and platform
);

CREATE INDEX idx_messages_campaign_id ON messages (campaign_id);
CREATE INDEX idx_messages_business_id ON messages (business_id);
CREATE INDEX idx_messages_contact_id ON messages (contact_id);
CREATE INDEX idx_messages_status ON messages (status);
```

**Notes:**
*   `platform` can be one of: `email`, `instagram`, `facebook`, `twitter`, `linkedin`.
*   `status` can be one of: `pending`, `sent`, `failed`, `opened`, `replied`.
*   `ON DELETE CASCADE` ensures that if a campaign, business, or contact is deleted, associated messages are also deleted.

## 5. Table: `users` (for authentication)

Stores user authentication information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users (username);
```

**Notes:**
*   `password_hash` will store a hashed version of the user's password.

## 6. Relationships

*   One `Business` can have many `Contacts`.
*   One `Campaign` can have many `Messages`.
*   One `Business` can be associated with many `Messages` (across different campaigns).
*   One `Contact` can be associated with many `Messages` (across different campaigns).

This schema provides a solid foundation for the platform's data storage needs. We will use SQLAlchemy ORM in the Flask backend to interact with this database.

