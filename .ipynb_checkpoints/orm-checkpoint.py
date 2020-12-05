def build_from_record(Class, record):
    if not record: return None

    attr = dict(zip(Class.attributes, record))
    obj = Class()
    obj.__dict__ = attr
    return obj

def build_from_records(Class, records):
    return [build_from_record(Class, record) for record in records]


def find_all(Class, cursor):
    sql_str = f"SELECT * FROM {Class.__table__}"
    cursor.execute(sql_str)
    records = cursor.fetchall()
    return [build_from_record(Class, record) for record in records]

def values(obj):
    venue_attrs = obj.__dict__
    return [venue_attrs[attr] for attr in obj.attributes if attr in venue_attrs.keys()]

def keys(obj):
    venue_attrs = obj.__dict__
    selected = [attr for attr in obj.attributes if attr in venue_attrs.keys()]
    return ', '.join(selected)


def save(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
    insert_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str});"""
    cursor.execute(insert_str, list(values(obj)))
    conn.commit()
    select_str = f"""SELECT  * FROM {obj.__table__} ORDER BY id DESC LIMIT 1"""
    cursor.execute(select_str)
    last_record = cursor.fetchone()
    return build_from_record(type(obj), last_record)
    



