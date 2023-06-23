#!/usr/bin/env python3

import os
import sys
import psycopg2

# Database connection details
db_url = os.environ.get('MARU_HOME_DB')

# Connect to the Postgres database
conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Function to fetch enum types
def get_enum_types():
    query = "SELECT typname FROM pg_type WHERE typtype = 'e'"
    cur.execute(query)
    rows = cur.fetchall()
    return rows

# Function to transform name to Golang notation
def transform_name(name):
    name_parts = name.split("_")
    transformed_name_parts = []
    for part in name_parts:
        if part.lower() != "enum":
            transformed_name_parts.append(part.capitalize())
    return "".join(transformed_name_parts)

# Function to generate Golang enum type
def generate_golang_enum(enum_name, enum_labels):
    transformed_name = transform_name(enum_name)
    golang_code = f"type {transformed_name} string\n\n"
    golang_code += f"const (\n"
    for enum_label in enum_labels:
        constant_name = transform_name(enum_label)
        golang_code += f"\t{transformed_name}{constant_name} {transformed_name} = \"{enum_label}\"\n"
    golang_code += f")\n"
    return golang_code

# Fetch enum types
enum_types = get_enum_types()

# Generate Golang enum types
generated_code = ""
for enum_type in enum_types:
    enum_name = enum_type[0]
    enum_labels_query = f"SELECT enumlabel FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = '{enum_name}')"
    cur.execute(enum_labels_query)
    enum_labels = [row[0] for row in cur.fetchall()]
    golang_enum_code = generate_golang_enum(enum_name, enum_labels)
    generated_code += golang_enum_code + "\n"

# Print the generated code
print("Generated Golang enum types:\n")
print(generated_code)

# Close the database connection
cur.close()
conn.close()
