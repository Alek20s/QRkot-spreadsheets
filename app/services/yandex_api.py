# app/services/yandex_api.py
from datetime import datetime, timedelta
from io import BytesIO
from typing import List

import pandas as pd

from app.core.yandex_client import YandexDiskClient
from app.models.charity_project import CharityProject

SECONDS_IN_DAY = 86400
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60

REPORT_COLUMNS = ('Название проекта', 'Время сбора', 'Описание')
DATA_START_ROW = 2


def format_time_delta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, SECONDS_IN_DAY)
    hours, remainder = divmod(remainder, SECONDS_IN_HOUR)
    minutes = remainder // SECONDS_IN_MINUTE

    if days:
        return f'{days} дн. {hours} ч.'
    return f'{hours} ч. {minutes} мин.'


async def create_simple_report(
    projects: List[CharityProject],
    client: YandexDiskClient,
    report_format: str,
) -> str:
    filename = f'report_{datetime.now().strftime(report_format)}.xlsx'
    upload_url, disk_path = await client.create_excel_file(filename)

    rows = [
        {
            'Название проекта': project.name,
            'Время сбора': format_time_delta(
                project.close_date - project.create_date
            ),
            'Описание': project.description,
        }
        for project in projects
    ]
    dataframe = pd.DataFrame(rows, columns=REPORT_COLUMNS)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(
            writer, sheet_name='Отчёт', index=False, startrow=1,
        )
        workbook = writer.book
        worksheet = writer.sheets['Отчёт']

        bold_format = workbook.add_format({'bold': True, 'border': 1})
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9D9D9',
            'border': 1,
        })
        cell_format = workbook.add_format({'border': 1})

        worksheet.write(
            0, 0,
            f'Отчёт от {datetime.now().strftime("%d.%m.%Y")}',
            bold_format,
        )
        for col, name in enumerate(dataframe.columns):
            worksheet.write(1, col, name, header_format)
        for row_idx in range(len(dataframe)):
            for col_idx in range(len(dataframe.columns)):
                worksheet.write(
                    row_idx + DATA_START_ROW, col_idx,
                    dataframe.iloc[row_idx, col_idx], cell_format,
                )

        total_row = len(dataframe) + DATA_START_ROW
        worksheet.write(total_row, 0, 'Итого проектов:', bold_format)
        worksheet.write(total_row, 1, len(dataframe), bold_format)

    output.seek(0)
    await client.upload_file(upload_url, output.read())
    return await client.publish_file(disk_path)
