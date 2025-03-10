@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("output", "-o", required=True, type=click.Path())
def main(filename, output):
    data: list[HCMHeader | HCMRecord] = []
    err_lines = 0

    with open(filename, mode="r", encoding=CSV_ENCODING) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=CSV_DELIMITER)
        for idx, row in enumerate(reader, start=1):
            # Interpret empty values as None (instead of '')
            row = {k: v if v else None for k, v in row.items()}
            d = {f"{HCM_FIELD_PREFIX}{k}": v for k, v in row.items()}
            try:
                record = HCMRecord(**d)
                data.append(record)
            except ValueError as e:
                l = f"Line {idx}"
                print(f"{l}\n{'-' * len(l)}\n{e}")
                err_lines += 1

    # TODO: how to configure the header ...
    header = HCMHeader(
        filenumber_medium=1,
        filenumber=1,
        fileversion=1.0,
        filecontent="abc",
        filetype="O",
        origin_country="AUT",
        destination_country="AUT",
        email="nobody@drei.at",
        phone="",
        fax="",
        person_name="Mr. Nobody",
        creation_date=f"{datetime.datetime.now():%m%d%Y}",
        record_count=len(data),
    )

    with open(output, "w") as f:
        print(header.model_dump(), file=f, end="")

        for record in data:
            print(record.model_dump(), file=f)
