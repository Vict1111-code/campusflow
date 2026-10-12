
def calculate_priority(urgency: str, affected_users: int) -> str:
    """Calculate ticket priority using the first matching rule."""

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"

def validate_title(title):
    if not isinstance(title, str):
        raise ValueError("Title must be a string.")
    
    title = title.strip()

    if not title:
        raise ValueError("Title cannot be empty.")

    return title

def validate_category(category):
    if not isinstance(category, str):
        raise ValueError("Category must be a string.")
    
    category = category.strip().lower()

    validate_categories = {
        "network": "Network",
        "software": "Software",
        "hardware": "Hardware",
        "other": "Other"
    }

    if category not in validate_categories:
        raise ValueError("Invalid ticket category")
    
    return validate_categories[category]

def validate_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a string.")

    urgency = urgency.strip().lower()

    valid_urgencies = ("low", "medium", "high")

    if urgency not in valid_urgencies:
        raise ValueError("Invalid ticket urgency")

    return urgency


def validate_affected_users(affected_users):
    if not isinstance(affected_users, int):
        raise ValueError("Affected users must be an integer.")

    if type(affected_users) is not int:
        raise ValueError("Affected users must be an integer, not a boolean.")
    
    if affected_users <= 0:
        raise ValueError("Affected users cannot be negative.")

    return affected_users

def generate_ticket_id(tickets):
    highest_number = 0

    for ticket in tickets:
        ticket_id = ticket["id"]

        number = int(ticket_id[1:])

        if number > highest_number:
            highest_number = number

    next_number = highest_number + 1

    return f"T{next_number:03d}"

def create_ticket(tickets, title, category, urgency, affected_users):
    validated_title = validate_title(title)
    validated_category = validate_category(category)
    validated_urgency = validate_urgency(urgency)
    validated_affected_users = validate_affected_users(affected_users)

    priority = calculate_priority(validated_urgency, validated_affected_users)

    ticket_id = generate_ticket_id(tickets)

    ticket = {
        "id": ticket_id,
        "title": validated_title,
        "category": validated_category,
        "urgency": validated_urgency,
        "affected_users": validated_affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }

    tickets.append(ticket)

    return ticket
    