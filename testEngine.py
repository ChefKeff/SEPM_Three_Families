from game_engine.testingComm import testing_comm

def test_engine(number_of_test: int = 500):
    testing_comm(number_of_test)

test_engine()