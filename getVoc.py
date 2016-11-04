# -*- coding: utf-8 -*-
import sqlalchemy
import xml.etree.ElementTree as ET
import vsptd


# TODO Переименовать переменные согласно PEP8


# # для БД на mssql
# def trp_get_voc_mssql(prefix, name, path):
#     engine = sqlalchemy.create_engine('mssql+pyodbc://PC-ALEX/P3375_K_SBD_5_1_Ushakov?driver=ODBC+Driver+11+for+SQL+Server')
#     query = sqlalchemy.text('SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name')
#     result = engine.execute(query,{"prefix": prefix, "name": name}).first()[0]
#     return vsptd.parse_triplex_string(result)
#
#
# # для БД на sqlite
# def trp_get_voc_sqlite(prefix, name, path):
#     engine = sqlalchemy.create_engine(r'sqlite:///' + t)
#     sql_query = 'SELECT LINK FROM OSl_test_1 WHERE OBJ=:prefix and NAME=:name'
#     result = engine.execute(sql_query, prefix=prefix, name=name).first()[0]
#     return vsptd.parse_triplex_string(result)


# для БД на sql
def trp_get_voc_sql(prefix, name, path):
    engine = sqlalchemy.create_engine(r'sqlite:///' + path)
    metadata = sqlalchemy.MetaData(engine)
    q_table = sqlalchemy.Table('Q', metadata, autoload=True)
    triplex_string = vsptd.TrpStr()
    for col in q_table.columns:
        export_prefix = str(col)[:1]
        export_name = str(col)[2:]
        sql_query = 'SELECT ' + export_name + ' FROM  ' + export_prefix + '  WHERE OBJ=:prefix and NAME=:name'
        result = engine.execute(sql_query, prefix=prefix, name=name).first()[0]
        if export_name != 'LINK':
            triplet = vsptd.Trp(export_prefix, export_name, result)
            triplex_string += triplet
        else:
            triplex_string += vsptd.parse_triplex_string(result)
    return triplex_string


# для БД на xml
def trp_get_voc_xml(prefix, name, path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    triplex_string = vsptd.TrpStr()
    triplex_string += vsptd.Trp('Q', 'OBJ', prefix)
    triplex_string += vsptd.Trp('Q', 'NAME', name)
    for r in root.findall('Rec'):
        export_prefix = r.find('OBJ').text
        export_name = r.find('NAME').text
        if export_prefix == prefix and export_name == name:
            frmt = r.find('FRMT').text
            triplex_string += vsptd.Trp('Q', 'FRMT', frmt)
            nm = r.find('NM').text
            triplex_string += vsptd.Trp('Q', 'NM', nm)
            k = r.find('K').text
            triplex_string += vsptd.Trp('Q', 'K', int(k))
            link = r.find('LINK').text
            triplex_string += vsptd.parse_triplex_string(link)
    return triplex_string