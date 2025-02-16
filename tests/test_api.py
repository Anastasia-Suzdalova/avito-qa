import pytest
import re

from host import Host
from datetime import datetime
from constants import (
    STATUS_KEY, CREATED_AT_KEY, SELLER_ID_KEY,
    PRICE_KEY, NAME_KEY, ID_KEY, CONTACTS_KEY,
    STATISTICS_KEY, LIKES_KEY, VIEW_COUNT_KEY,
)


SELLER_ID = 515515
host = Host()


def extract_uuid(text):
    pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    else:
        return None


def inc_last_letter(uuid):
    new_last_letter: str = "a"
    last_letter = uuid[-1]
    if last_letter.isdigit():
        new_last_letter = str((int(uuid[-1]) + 1) % 10)
    else:
        if last_letter == "z":
            new_last_letter = "a"
        else:
            new_last_letter = chr(ord(last_letter) + 1)
    uuid = uuid[:-1] + new_last_letter
    return uuid


def parse_time(time):
    time = time[:-6]  # нужно ли убирать лишний часовой пояс или баг?
    date_format = '%Y-%m-%d %H:%M:%S.%f %z'
    dt = datetime.strptime(time, date_format)
    return dt


def test_create_item():
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)

    assert resp.status_code == 200
    assert len(resp.json()[STATUS_KEY]) != 0


@pytest.mark.skip("баг -- приходит 200")
def test_create_item_without_req_field():
    # сначала уберем seller id
    data = {
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

    # попробуем убрать name
    data = {
        "sellerID": SELLER_ID,
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

    # попробуем убрать price
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400


def test_create_item_unexpected_map_type():
    # сначала передадим в seller id не число
    data = {
        "sellerID": str(SELLER_ID),
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

    # передадим в name число
    data = {
        "sellerID": SELLER_ID,
        "name": 500,
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

     # передадим в price строку
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": str(500),
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400


@pytest.mark.skip("баг? -- может ли быть отрицательным seller id -- серая зона")
def test_create_item_negative_seller_id():
    # передадим отрицательный seller id
    data = {
        "sellerID": -SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400


@pytest.mark.skip("баг? -- может ли быть отрицательным price -- серая зона")
def test_create_item_negative_price():
    # передадим отрицательный price
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": -500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400


def test_create_item_unexpected_map_type():
    # сначала передадим в seller id не число
    data = {
        "sellerID": str(SELLER_ID),
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

    # передадим в name число
    data = {
        "sellerID": SELLER_ID,
        "name": 500,
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400

     # передадим в price строку
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": str(500),
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 400


def test_create_two_diff_items():
    # создадим 2 объявления подряд, проверим
    # что у них не совпадают id
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid1 = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid1 is not None

    resp = host.create_item(data=data)
    assert resp.status_code == 200
    uuid2 = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid2 is not None

    assert uuid1 != uuid2


def test_get_item_info():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200


def test_get_item_info_check_uuid():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    assert resp.json()[0][ID_KEY] == uuid


@pytest.mark.skip("баг -- имя не соответствует переданному")
def test_get_item_info_check_name():
    name = "item1"
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": name,
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    assert resp.json()[0][NAME_KEY] == name


def test_get_item_info_check_price():
    price = 5123
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": price,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    assert resp.json()[0][PRICE_KEY] == price


def test_get_item_info_check_seller_id():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    assert resp.json()[0][SELLER_ID_KEY] == SELLER_ID


def test_get_item_info_check_created_at():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлениях
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    if CREATED_AT_KEY in resp.json()[0]:
        dt = parse_time(resp.json()[0][CREATED_AT_KEY])
        dt_now = datetime.now()
        assert dt.day == dt_now.day
        assert dt.month == dt_now.month
        assert dt.year == dt_now.year


def test_get_item_info_get_statistics():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # получим информацию об объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # т.к. объект nullable, то сначала проверим,
    # есть ли он в ответе
    if STATISTICS_KEY in resp.json()[0]:
        stat_map = resp.json()[0][STATISTICS_KEY]
        assert LIKES_KEY in stat_map
        assert VIEW_COUNT_KEY in stat_map
        assert CONTACTS_KEY in stat_map

        assert isinstance(stat_map[LIKES_KEY], int)
        assert isinstance(stat_map[VIEW_COUNT_KEY], int)
        assert isinstance(stat_map[CONTACTS_KEY], int)


def test_get_item_info_empty_uuid():
    # не передадим id
    resp = host.get_item_info(id="")
    assert resp.status_code == 404


def test_get_item_info_unexpected_uuid():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # заменим последнюю букву на следующую
    uuid = inc_last_letter(uuid)

    # получим информацию о несуществующем объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 404


@pytest.mark.skip("серая зона, какой код должен быть при несоответствии формата?")
def test_get_item_info_not_uuid():
    # получим информацию об объявлении
    # в запросе передаем не в формате uuid
    resp = host.get_item_info(id="some-uuid")
    assert resp.status_code == 400


@pytest.mark.skip("баг -- не проходит, не ищет объявление по uuid")
def test_get_item_statistics():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    resp = host.get_item_statistics(id=uuid)
    assert resp.status_code == 200
    # т.к. объект nullable, то сначала проверим,
    # есть ли он в ответе
    if STATISTICS_KEY in resp.json():
        stat_map = resp.json()[STATISTICS_KEY]
        assert LIKES_KEY in stat_map
        assert VIEW_COUNT_KEY in stat_map
        assert CONTACTS_KEY in stat_map

        assert isinstance(stat_map[LIKES_KEY], int)
        assert isinstance(stat_map[VIEW_COUNT_KEY], int)
        assert isinstance(stat_map[CONTACTS_KEY], int)


def test_get_item_statistics_empty_uuid():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    resp = host.get_item_statistics(id="")
    assert resp.status_code == 404


def test_get_item_statistics_unexpected_uuid():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    # заменим последнюю букву на следующую
    uuid = inc_last_letter(uuid)

    # получим информацию о несуществующем объявлении
    resp = host.get_item_info(id=uuid)
    assert resp.status_code == 404


@pytest.mark.skip("серая зона, какой код должен быть при несоответствии формата?")
def test_get_item_statistics_not_uuid():
    # получим информацию об объявлении с некорректным uuid
    resp = host.get_item_info(id="some_uuid")
    assert resp.status_code == 400


def test_get_seller_items():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0


@pytest.mark.skip("баг -- имя не соответствует передаваемому")
def test_get_seller_items_check_name():
    name = "item1"
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": name,
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # интересует объявление, которое только что добавили
    last_idx = len(resp.json()) - 1
    assert resp.json()[last_idx][NAME_KEY] == name


@pytest.mark.skip("баг -- id не соответствует передаваемому")
def test_get_seller_items_check_uuid():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # интересует объявление, которое только что добавили
    last_idx = len(resp.json()) - 1
    assert resp.json()[last_idx][ID_KEY] == uuid


def test_get_seller_items_check_price():
    price = 5123
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": price,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # интересует объявление, которое только что добавили
    last_idx = len(resp.json()) - 1
    assert resp.json()[last_idx][PRICE_KEY] == price


def test_get_seller_items_check_statistics():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    uuid = extract_uuid(resp.json()[STATUS_KEY])
    assert uuid is not None

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # интересует объявление, которое только что добавили
    last_idx = len(resp.json()) - 1
    # т.к. объект nullable, то сначала проверим,
    # есть ли он в ответе
    if STATISTICS_KEY in resp.json()[last_idx]:
        stat_map = resp.json()[last_idx][STATISTICS_KEY]
        assert LIKES_KEY in stat_map
        assert VIEW_COUNT_KEY in stat_map
        assert CONTACTS_KEY in stat_map

        assert isinstance(stat_map[LIKES_KEY], int)
        assert isinstance(stat_map[VIEW_COUNT_KEY], int)
        assert isinstance(stat_map[CONTACTS_KEY], int)


def test_get_seller_items_check_created_at():
    # создадим объявление
    data = {
        "sellerID": SELLER_ID,
        "name": "item1",
        "price": 500,
    }
    resp = host.create_item(data=data)
    assert resp.status_code == 200

    resp = host.get_seller_items(seller_id=SELLER_ID)
    assert resp.status_code == 200
    assert len(resp.json()) > 0

    # интересует объявление, которое только что добавили
    last_idx = len(resp.json()) - 1
    if CREATED_AT_KEY in resp.json()[last_idx]:
        dt = parse_time(resp.json()[last_idx][CREATED_AT_KEY])
        dt_now = datetime.now()
        assert dt.day == dt_now.day
        assert dt.month == dt_now.month
        assert dt.year == dt_now.year
