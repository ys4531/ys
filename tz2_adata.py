import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_registry(base_url, num_pages):
    potential_supplier_names = []
    bin_iins = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all("tr")

            for row in rows[
                1:
            ]:  # Пропускаем заголовок таблицы, начинаем с первой строки данных
                cols = row.find_all("td")

                potential_supplier_names.append(cols[1].text.strip())
                bin_iins.append(cols[2].text.strip())

    df = pd.DataFrame(
        {
            "Наименование потенциального поставщика": potential_supplier_names,
            "БИН/ИИН": bin_iins,
        }
    )

    return df


def main():
    base_url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=50&page="
    num_pages = 12  # Необходимо установить реальное количество страниц

    df = parse_registry(base_url, num_pages)
    df = df.drop_duplicates()

    if df is not None and not df.empty:
        df.to_excel("registry_data.xlsx", index=False)
        print("Данные успешно сохранены в файл registry_data.xlsx")
    else:
        print("Не удалось получить данные")


if __name__ == "__main__":
    main()