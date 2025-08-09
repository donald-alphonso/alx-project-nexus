-- =====================================================
-- SOCIAL MEDIA BACKEND - DATABASE SCHEMA
-- ALX Project Nexus - Django Models to SQL
-- =====================================================

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    bio TEXT,
    avatar VARCHAR(100),
    birth_date DATE,
    location VARCHAR(100),
    website VARCHAR(200),
    is_verified BOOLEAN DEFAULT FALSE,
    followers_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    posts_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. FOLLOWS TABLE (User-to-User M:N relationship)
-- =====================================================
CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    following_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(follower_id, following_id)
);

-- =====================================================
-- 3. POSTS TABLE
-- =====================================================
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    image VARCHAR(100),
    video VARCHAR(100),
    visibility VARCHAR(10) DEFAULT 'public' CHECK (visibility IN ('public', 'followers', 'private')),
    is_pinned BOOLEAN DEFAULT FALSE,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. COMMENTS TABLE
-- =====================================================
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE, -- Self-reference for replies
    content TEXT NOT NULL,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 5. HASHTAGS TABLE
-- =====================================================
CREATE TABLE hashtags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    posts_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 6. POST_HASHTAGS TABLE (Post-to-Hashtag M:N relationship)
-- =====================================================
CREATE TABLE post_hashtags (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    hashtag_id INTEGER REFERENCES hashtags(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(post_id, hashtag_id)
);

-- =====================================================
-- 7. LIKES TABLE (Polymorphic - can like posts or comments)
-- =====================================================
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    content_type_id INTEGER, -- Points to ContentType (Django concept)
    object_id INTEGER, -- Points to Post.id or Comment.id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_type_id, object_id)
);

-- =====================================================
-- 8. SHARES TABLE
-- =====================================================
CREATE TABLE shares (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    share_type VARCHAR(10) DEFAULT 'repost' CHECK (share_type IN ('repost', 'quote', 'share')),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)
);

-- =====================================================
-- 9. BOOKMARKS TABLE
-- =====================================================
CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)
);

-- =====================================================
-- 10. NOTIFICATIONS TABLE
-- =====================================================
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(10) CHECK (notification_type IN ('like', 'comment', 'share', 'follow', 'mention', 'reply')),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    content_type_id INTEGER, -- Polymorphic relation
    object_id INTEGER, -- Polymorphic relation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 11. REPORTS TABLE
-- =====================================================
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    reporter_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    reason VARCHAR(15) CHECK (reason IN ('spam', 'harassment', 'hate_speech', 'violence', 'inappropriate', 'copyright', 'other')),
    description TEXT,
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved', 'dismissed')),
    content_type_id INTEGER, -- Polymorphic relation
    object_id INTEGER, -- Polymorphic relation
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Users indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Posts indexes
CREATE INDEX idx_posts_author_created ON posts(author_id, created_at DESC);
CREATE INDEX idx_posts_visibility_created ON posts(visibility, created_at DESC);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Comments indexes
CREATE INDEX idx_comments_post_created ON comments(post_id, created_at);
CREATE INDEX idx_comments_author_created ON comments(author_id, created_at DESC);
CREATE INDEX idx_comments_parent ON comments(parent_id);

-- Follows indexes
CREATE INDEX idx_follows_follower ON follows(follower_id);
CREATE INDEX idx_follows_following ON follows(following_id);

-- Hashtags indexes
CREATE INDEX idx_hashtags_name ON hashtags(name);
CREATE INDEX idx_hashtags_posts_count ON hashtags(posts_count DESC);

-- Likes indexes
CREATE INDEX idx_likes_content ON likes(content_type_id, object_id);
CREATE INDEX idx_likes_user_created ON likes(user_id, created_at DESC);

-- Notifications indexes
CREATE INDEX idx_notifications_recipient_created ON notifications(recipient_id, created_at DESC);
CREATE INDEX idx_notifications_recipient_read ON notifications(recipient_id, is_read);

-- Reports indexes
CREATE INDEX idx_reports_status_created ON reports(status, created_at DESC);
CREATE INDEX idx_reports_content ON reports(content_type_id, object_id);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample users
INSERT INTO users (username, email, first_name, last_name, bio) VALUES
('alice', 'alice@example.com', 'Alice', 'Johnson', 'Photography enthusiast'),
('bob', 'bob@example.com', 'Bob', 'Smith', 'Tech blogger'),
('charlie', 'charlie@example.com', 'Charlie', 'Brown', 'Travel lover');

-- Insert sample posts
INSERT INTO posts (author_id, content, visibility) VALUES
(1, 'Beautiful sunset today! #photography #nature', 'public'),
(2, 'New trends in web development for 2025 #tech #webdev', 'public'),
(3, 'Just arrived in Paris! Amazing city #travel #paris', 'followers');

-- Insert sample hashtags
INSERT INTO hashtags (name, posts_count) VALUES
('photography', 1),
('nature', 1),
('tech', 1),
('webdev', 1),
('travel', 1),
('paris', 1);

-- Insert sample follows
INSERT INTO follows (follower_id, following_id) VALUES
(2, 1), -- Bob follows Alice
(3, 1), -- Charlie follows Alice
(1, 3); -- Alice follows Charlie

-- Insert sample comments
INSERT INTO comments (post_id, author_id, content) VALUES
(1, 2, 'Amazing shot, Alice!'),
(1, 3, 'Love the colors in this photo'),
(2, 1, 'Great insights on web development');

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View: User stats with follower/following counts
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.followers_count,
    u.following_count,
    u.posts_count,
    COUNT(DISTINCT p.id) as actual_posts_count,
    COUNT(DISTINCT f1.id) as actual_followers_count,
    COUNT(DISTINCT f2.id) as actual_following_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
LEFT JOIN follows f1 ON u.id = f1.following_id
LEFT JOIN follows f2 ON u.id = f2.follower_id
GROUP BY u.id, u.username, u.email, u.followers_count, u.following_count, u.posts_count;

-- View: Post engagement stats
CREATE VIEW post_engagement AS
SELECT 
    p.id,
    p.content,
    p.author_id,
    u.username as author_username,
    p.likes_count,
    p.comments_count,
    p.shares_count,
    COUNT(DISTINCT c.id) as actual_comments_count,
    COUNT(DISTINCT s.id) as actual_shares_count,
    p.created_at
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
LEFT JOIN shares s ON p.id = s.post_id
GROUP BY p.id, p.content, p.author_id, u.username, p.likes_count, p.comments_count, p.shares_count, p.created_at;

-- =====================================================
-- TRIGGERS FOR MAINTAINING COUNTS
-- =====================================================

-- Trigger to update followers_count when follow is added/removed
CREATE OR REPLACE FUNCTION update_follower_counts()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Increase following_count for follower
        UPDATE users SET following_count = following_count + 1 WHERE id = NEW.follower_id;
        -- Increase followers_count for followed user
        UPDATE users SET followers_count = followers_count + 1 WHERE id = NEW.following_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        -- Decrease following_count for follower
        UPDATE users SET following_count = following_count - 1 WHERE id = OLD.follower_id;
        -- Decrease followers_count for followed user
        UPDATE users SET followers_count = followers_count - 1 WHERE id = OLD.following_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_follower_counts
    AFTER INSERT OR DELETE ON follows
    FOR EACH ROW EXECUTE FUNCTION update_follower_counts();

-- =====================================================
-- END OF SCHEMA
-- =====================================================
