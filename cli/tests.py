from backend.db_engine import DocumentDb

def test_open_db():
    document = DocumentDb()
    assert type(document.db) == list, "db must be a list instance"

def test_get():
    document = DocumentDb()
    response = document.get("dmd")
    assert type(response) == list

def test_get_with_path():
    document = DocumentDb()
    response = document.get("dmd.asked")
    assert type(response) == list

def test_get_with_path_and_filter():
    document = DocumentDb()
    response = document.get("dmd.commands", "name like deploy")
    assert type(response) == list

def test_add_new_cmd():
    document = DocumentDb()
    response = document.add_cmd("dmd", "pods", "test", "kubectl get pods")
    assert type(response) == dict

def test_add_new_project_and_cmd():
    document = DocumentDb()
    response = document.add_cmd("rendalo", "gp", "deploy k8 infra", "kubectl get pods")
    assert type(response) == dict

if __name__ == "__main__":
    test_open_db()
    test_get()
    test_get_with_path()
    test_get_with_path_and_filter()
    #test_add_new_cmd()
    test_add_new_project_and_cmd()