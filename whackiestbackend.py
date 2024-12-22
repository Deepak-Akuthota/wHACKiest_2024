import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Connect to the database
    conn.row_factory = sqlite3.Row  # To fetch rows as dictionaries
    return conn

# Preprocess data: converts interests from list to comma-separated string
def preprocess_data(data):
    if isinstance(data['interests'][0], list):  # Only join if 'interests' is a list of lists
        data['interests'] = [','.join(interests) for interests in data['interests']]
    return data

# Function to fetch all users and their data from the database
def fetch_user_data():
    conn = get_db_connection()
    query = '''
    SELECT u.id, u.age, u.location, u.education, GROUP_CONCAT(i.interest) AS interests
    FROM users u
    JOIN user_interests ui ON u.id = ui.user_id
    JOIN interests i ON ui.interest_id = i.id
    GROUP BY u.id;
    '''
    users = conn.execute(query).fetchall()
    conn.close()

    # Convert fetched data to a pandas DataFrame
    data = {
        'id': [user['id'] for user in users],
        'age': [user['age'] for user in users],
        'location': [user['location'] for user in users],
        'education': [user['education'] for user in users],
        'interests': [user['interests'].split(',') for user in users]
    }

    return pd.DataFrame(data)

# Function to find matching people based on interests
def match_people(user_data, database_df):
    matching_columns = list(database_df.columns)  # Get all columns from database_df

    # Add an 'id' to user_data so that it matches the columns expected
    user_data['id'] = 0  # Placeholder ID for user_data (you can modify this if needed)
    
    # Convert user data to a DataFrame
    user_df = pd.DataFrame([user_data])

    # Select relevant columns for matching
    user_matching_df = user_df[matching_columns]
    database_matching_df = database_df[matching_columns]

    # One-hot encode categorical variables and align columns
    user_matching_df = pd.get_dummies(user_matching_df)
    database_matching_df = pd.get_dummies(database_matching_df)

    all_columns = set(user_matching_df.columns).union(set(database_matching_df.columns))
    user_matching_df = user_matching_df.reindex(columns=all_columns, fill_value=0)
    database_matching_df = database_matching_df.reindex(columns=all_columns, fill_value=0)

    # Normalize numerical columns (e.g., age)
    if 'age' in matching_columns:
        scaler = MinMaxScaler()
        database_matching_df['age'] = scaler.fit_transform(database_matching_df[['age']])
        user_matching_df['age'] = scaler.transform(user_matching_df[['age']])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_matching_df, database_matching_df)

    # Get IDs of matched people
    matched_people = []
    threshold = similarity_scores.mean() + similarity_scores.std() * 0.5  # Dynamic threshold
    for i, score in enumerate(similarity_scores[0]):
        score_percentage = score * 100  # Convert to percentage
        if score_percentage > (threshold * 100):  # Adjust threshold to percentage scale
            matched_people.append((database_df.index[i], round(score_percentage, 2)))  # Round for readability

    return matched_people

# Sample user data to match
user_data = {
    'age': 30,
    'interests': ['reading', 'hiking', 'music'],
    'location': 'New York',
    'education': 'Bachelor'
}

# Preprocess the user data
user_data['interests'] = ','.join(user_data['interests'])

# Fetch the data from the SQL database
database_df = fetch_user_data()

# Find matches
matched_people = match_people(user_data, database_df)

# Print the matched people
for person_id, score in matched_people:
    print(f"Person number: {person_id} is matched\nSimilarity score: {score}\n")
