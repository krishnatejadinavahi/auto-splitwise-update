from splitwise import Splitwise, Expense
import webbrowser
from splitwise.group import Group
from splitwise.user import ExpenseUser, User

from splitwiseapp.splitwise_redis_utils import SplitwiseRedisUtils


class SplitwiseApiUtils(SplitwiseRedisUtils):
    splitwise_request_object = []
    url = None
    secret = None
    consumer_key = "q4wvovzsxjeS9R4ERB6ICqWUgPNK0awUQYbumMEi"
    consumer_secret = "ccot2M24EG5tUaCFYOtC5oBoMmsy0HoytA8swuoV"
    splitwise_obj = None
    splitwise_friend = None

    def post_transactions_to_splitwise(self, oauth_token, oauth_verifier):
        access_token = SplitwiseApiUtils.splitwise_obj.getAccessToken(oauth_token, SplitwiseApiUtils.secret,
                                                                      oauth_verifier)
        SplitwiseApiUtils.splitwise_obj.setAccessToken(access_token)
        self.create_group_if_not_exists()

        current_user_id = SplitwiseApiUtils.splitwise_obj.getCurrentUser().id
        friend_obj = self.get_friend(SplitwiseApiUtils.splitwise_obj.getFriends())

        group_id = self.client.get(f"sw-${current_user_id}")
        user1 = ExpenseUser()
        user1.setId(current_user_id)

        user2 = ExpenseUser()
        user2.setId(friend_obj.id)

        self.create_expense_on_splitwise(group_id, user1, user2)

    def create_expense_on_splitwise(self, group_id, user1, user2):
        for transaction in SplitwiseApiUtils.splitwise_request_object:
            expense = Expense()
            transaction_cost = float(transaction['amount'][1:])
            expense.setCost(transaction_cost)
            expense.setDescription(transaction['merchant'])
            expense.details = f"Expense made on {transaction['date']} using {transaction['card']}"
            expense.group_id = int(group_id.decode('utf-8'))

            user1.setPaidShare(transaction_cost)
            user1.setOwedShare('0.00')

            user2.setPaidShare('0.00')
            user2.setOwedShare(transaction_cost)

            users = [user1, user2]

            expense.setUsers(users)

            SplitwiseApiUtils.splitwise_obj.createExpense(expense)

    def create_group_if_not_exists(self):
        current_user_id = SplitwiseApiUtils.splitwise_obj.getCurrentUser().id

        group_from_redis = self.client.get(f"sw-${current_user_id}")

        if not group_from_redis:
            group = Group()
            group.setName("Auto-Splitwise")
            friend_obj = self.get_friend(SplitwiseApiUtils.splitwise_obj.getFriends())

            friend1 = User()
            friend1.setId(friend_obj.id)

            current_user_id = SplitwiseApiUtils.splitwise_obj.getCurrentUser().id

            user1 = User()
            user1.setId(current_user_id)

            users = [user1, friend1]
            group.setMembers(users)

            group_created = SplitwiseApiUtils.splitwise_obj.createGroup(group)
            group_id = group_created.id
            self.store_group_id_for_user(group_id, current_user_id)

    def get_or_request_splitwise_creds(self, request_to_splitwise):
        SplitwiseApiUtils.splitwise_request_object = request_to_splitwise['list_to_splitwise']
        SplitwiseApiUtils.splitwise_friend = request_to_splitwise['splitwise_friend']

        sObj = Splitwise(SplitwiseApiUtils.consumer_key, SplitwiseApiUtils.consumer_secret)
        SplitwiseApiUtils.splitwise_obj = sObj
        SplitwiseApiUtils.url, SplitwiseApiUtils.secret = sObj.getAuthorizeURL()
        webbrowser.open_new_tab(SplitwiseApiUtils.url)

    def get_friend(self, friend_list):
        return next((friend for friend in friend_list if friend.email == SplitwiseApiUtils.splitwise_friend), None)
