from locust import TaskSet, FastHttpUser, task, constant_throughput

test_data = {
	"float_features": [
		{
			"engines": 2,
			"passenger_capacity": 4,
			"crew": 3,
			"company_rating": 1,
			"review_scores_rating": 96
		},
		{
			"engines": 4,
			"passenger_capacity": 8,
			"crew": 5,
			"company_rating": 1,
			"review_scores_rating": 100
		},
		{
			"engines": 2,
			"passenger_capacity": 4,
			"crew": 3,
			"company_rating": 1,
			"review_scores_rating": 96
		},
		{
			"engines": 4,
			"passenger_capacity": 8,
			"crew": 5,
			"company_rating": 1,
			"review_scores_rating": 100
		},
		{
			"engines": 2,
			"passenger_capacity": 4,
			"crew": 3,
			"company_rating": 1,
			"review_scores_rating": 96
		},
		{
			"engines": 4,
			"passenger_capacity": 8,
			"crew": 5,
			"company_rating": 1,
			"review_scores_rating": 100
		},
		{
			"engines": 2,
			"passenger_capacity": 4,
			"crew": 3,
			"company_rating": 1,
			"review_scores_rating": 96
		},
		{
			"engines": 4,
			"passenger_capacity": 8,
			"crew": 5,
			"company_rating": 1,
			"review_scores_rating": 100
		}
	],
	"categorical_features": [
		{
			"d_check_complete": "False",
			"moon_clearance_complete": "False",
			"iata_approved": "True"
		},
		{
			"d_check_complete": "True",
			"moon_clearance_complete": "False",
			"iata_approved": "False"
		},
		{
			"d_check_complete": "False",
			"moon_clearance_complete": "False",
			"iata_approved": "True"
		},
		{
			"d_check_complete": "True",
			"moon_clearance_complete": "False",
			"iata_approved": "False"
		},
		{
			"d_check_complete": "False",
			"moon_clearance_complete": "False",
			"iata_approved": "True"
		},
		{
			"d_check_complete": "True",
			"moon_clearance_complete": "False",
			"iata_approved": "False"
		},
		{
			"d_check_complete": "False",
			"moon_clearance_complete": "False",
			"iata_approved": "True"
		},
		{
			"d_check_complete": "True",
			"moon_clearance_complete": "False",
			"iata_approved": "False"
		}
	]
}

class TestTasks(TaskSet):
    def on_start(self):
        self.test_data = test_data

    def predict(self, data):
        self.client.post(path="/predict",
                         headers={
                             "Content-Type": "application/json",
                             "Postman-Token": "9a75cc9b-f940-40a0-9cb0-f02986e1e16d",
                             "cache-control": "no-cache",
                             "token": "1337"
                         },
                         json=data)

    @task(1)
    def scenario(self):
        self.predict(self.test_data)

class TestUser(FastHttpUser):
    host = "http://api:80"
    wait_time = constant_throughput(1000)
    tasks = [TestTasks]