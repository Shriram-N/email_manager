import json
import requests
from googleapiclient.errors import HttpError
from authenticate.authenticate import Authenticate
from db.db_manager import DbManager
from condition import GreaterThanCondition, LessThanCondition, DoesNotEqualCondition, EqualsCondition, DoesNotContainCondition, ContainsCondition
from actions import MarkAsRead, MarkAsUnread


class ProcessEmail:
    def __init__(self, auth, db_manager):
        self.auth = auth
        self.db_manager = db_manager
        self.actions = {
            'mark as read': MarkAsRead(db_manager, auth),
            'mark as unread': MarkAsUnread(db_manager, auth)
        }
        self.conditions = {
            'contains': ContainsCondition,
            'does not contain': DoesNotContainCondition,
            'equals': EqualsCondition,
            'does not equal': DoesNotEqualCondition,
            'less than': LessThanCondition,
            'greater than': GreaterThanCondition
        }

    def apply_action(self, email, action_name):
        action = self.actions.get(action_name)
        if action:
            action.apply(email)

    def process_rules(self, rules):
        emails = self.db_manager.get_emails()
        for email in emails:
            for rule in rules:
                conditions = [self.conditions[cond['predicate']](cond['field'], cond['predicate'], cond['value']) for cond in rule['conditions']]
                actions = rule['actions']
                if rule['predicate'] == 'all':
                    if all(condition.matches(email) for condition in conditions):
                        for action in actions:
                            self.apply_action(email, action)
                elif rule['predicate'] == 'any':
                    if any(condition.matches(email) for condition in conditions):
                        for action in actions:
                            self.apply_action(email, action)

    def process_emails(self, rules_path):
        with open(rules_path) as json_file:
            rules = json.load(json_file)
        self.process_rules(rules)


if __name__ == "__main__":
    auth = Authenticate()
    db_manager = DbManager()
    process_email = ProcessEmail(auth, db_manager)
    process_email.process_emails('rules/rules.json')
