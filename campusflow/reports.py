
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def get_report(tickets):
    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in STATUSES},
        "by_priority": {priority: 0 for priority in PRIORITIES},
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"].lower()

        if status not in report["by_status"]:
            raise ValueError(f"Unknown status: {status}")

        if priority not in report["by_priority"]:
            raise ValueError(f"Unknown priority: {priority}")

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report

