# app/services/yandex_api.py
from datetime import datetime, timedelta
from io import BytesIO
from typing import List

import xlsxwriter

from app.core.yandex_client import YandexDiskClient
from app.models.charity_project import CharityProject

SECONDS_IN_DAY = 86400
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60


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

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Отчёт')

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

    headers = ('Название проекта', 'Время сбора', 'Описание')
    for col, header in enumerate(headers):
        worksheet.write(1, col, header, header_format)

    row = 2
    for project in projects:
        time_delta = format_time_delta(
            project.close_date - project.create_date
        )
        worksheet.write(row, 0, project.name, cell_format)
        worksheet.write(row, 1, time_delta, cell_format)
        worksheet.write(row, 2, project.description, cell_format)
        row += 1

    worksheet.write(row, 0, 'Итого проектов:', bold_format)
    worksheet.write(row, 1, len(projects), bold_format)

    workbook.close()
    output.seek(0)

    await client.upload_file(upload_url, output.read())
    return await client.publish_file(disk_path)
