from config.Static import Static
from window.WindUsers import WindUsers
from components.Grid import Grid
from db.collections.UsersCollection import UsersCollection
from window.WindDelUsers import WindDelUsers

class TasksController:
    def __init__(self, this):
        self.this = this

        self._static_ = Static()

    def create_user(self):
        wind = WindUsers(self.this._db_, "new")
        wind.exec_()
        
        if wind.state:
            wind.state = False
            grid = Grid(parent=self.this, table_name="tasks", is_tab=True, state=False)
            self.this.tabs_table.set_tab(wind.user["full_name"], grid)
            self.this.tabs_id[wind.user["full_name"]] = wind.user["_id"]
            grid.render_tables_tab()

    def set_tabs(self):
        col_users = UsersCollection(self.this._db_)
        users = col_users.read_all()

        for user in users:
            grid = Grid(parent=self.this, table_name="tasks",is_tab=True, state=False)
            self.this.tabs_table.set_tab(user["full_name"], grid)
            self.this.tabs_id[user["full_name"]] = user["_id"]
            grid.render_tables_tab()

    def delete_users(self):
        wind = WindDelUsers(self.this, self.this._db_)
        wind.exec_()
