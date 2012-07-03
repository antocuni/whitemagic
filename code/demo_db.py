import py
from magic import Database

MODEL_PY = str(py.path.local(__file__).dirpath('model3.py'))


def main():
    db1 = Database('sqlite:///db1.sqlite', MODEL_PY)
    db2 = Database('sqlite:///db2.sqlite', MODEL_PY)
    db1.create_all()
    db2.create_all()
    u1 = db1.model.User(name=u'antocuni', age=30)
    u2 = db2.model.User(name=u'foobar', age=42)
    db1.commit()
    db2.commit()


if __name__ == '__main__':
    main()
