-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    location TEXT,
    education TEXT
);

-- Create interests table
CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interest TEXT
);

-- Create user_interests table (many-to-many relationship between users and interests)
CREATE TABLE IF NOT EXISTS user_interests (
    user_id INTEGER,
    interest_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (interest_id) REFERENCES interests(id),
    PRIMARY KEY (user_id, interest_id)
);

-- Insert sample data into the users table
INSERT INTO users (age, location, education) VALUES
(28, 'New York', 'Bachelor'),
(32, 'Los Angeles', 'Master'),
(25, 'London', 'Bachelor'),
(30, 'New York', 'Bachelor'),
(27, 'Tokyo', 'Master');

-- Insert sample interests into the interests table
INSERT INTO interests (interest) VALUES
('reading'),
('hiking'),
('music'),
('gaming'),
('movies'),
('sports'),
('art'),
('cooking'),
('travel'),
('dancing');

-- Insert user interests into the user_interests table
INSERT INTO user_interests (user_id, interest_id) VALUES
(1, 1), (1, 2), (1, 3),  -- User 1: reading, hiking, music
(2, 4), (2, 5), (2, 6),  -- User 2: gaming, movies, sports
(3, 7), (3, 8), (3, 9),  -- User 3: art, cooking, travel
(4, 3), (4, 2), (4, 10), -- User 4: music, hiking, dancing
(5, 5), (5, 6), (5, 4);  -- User 5: movies, sports, gaming
