# -*- coding: utf-8 -*-
"""Module String"""

# import pandas as pd
import pdftableextract as pdf

import re

import pprint
pp = pprint.PrettyPrinter(depth=6)

pdf_file_name = "example.pdf"


def set_dict_val(_dict, _keys, _val):
    """Class docstring"""
    kl = _keys.split('|')
    v = kl[-1]
    reduce(lambda d, k: d.setdefault(k, {}), kl[:-1], _dict)[v] = _val


def get_dict_val(_dict, _keys):
    """Class docstring"""
    return reduce(lambda d, k: d.get(k, None), _keys.split('|'), _dict)


class EgrulNalogRuPdf(object):
    """Class docstring"""

    __NUM_OF_FTR_LINES = 1
    __NUM_OF_HDR_LINES = 0
    __NUM_OF_HDR_LINES_HDR_PAGE = 3

    __ENTITY_TYPE__NALOG_RU_PDF = {
        "ЕДИНЫЙ ГОСУДАРСТВЕННЫЙ РЕЕСТР ЮРИДИЧЕСКИХ ЛИЦ": "ul",
        "ЕДИНЫЙ ГОСУДАРСТВЕННЫЙ РЕЕСТР ИНДИВИДУАЛЬНЫХ ПРЕДПРИНИМАТЕЛЕЙ": {
            "Сведения об индивидуальном предпринимателе": "ip",
            "Сведения о крестьянском (фермерском) хозяйстве, главой которого "
            "является": "kfh"
        }
    }

    class RowParser(object):
        """Docstring"""

        __EGRUL_SCHEMA__NALOG_RU_PDF = {
            "Наименование": {
                "Полное наименование": "full_name",
                "Сокращенное наименование": "short_name",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            "Адрес (место нахождения)": {
                "Почтовый индекс": "address|postal_code",
                "Субъект Российской Федерации": "address|region",
                "Район (улус и т.п.)": "address|neighbour",
                "Населенный пункт (село и т.п.)": "address|place",
                "Город (волость и т.п.)": "address|city",
                "Улица (проспект, переулок и т.д.)": "address|street",
                "Дом (владение и т.п.)": "address|building",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            "Сведения о регистрации": {
                # "Способ образования": [],
                "ОГРН": "ogrn",
                # "Дата присвоения ОГРН": [],
                # "Дата регистрации": [],
                # "Регистрационный номер, присвоенный до 1 июля 2002 года": [],
                # "Наименование органа, зарегистрировавшего юридическое лицо "\
                # "до 1 июля 2002 года": [],
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            # "Сведения о регистрирующем органе по месту нахождения юридического "\
            # "лица": {
            #    "Наименование регистрирующего органа": [],
            #    "Адрес регистрирующего органа": [],
            #    "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
            #    "сведения": [["grn", "date"], ["STRING", "DATE"]]
            # },
            "Сведения об учете в налоговом органе": {
                "ИНН": "tax|inn",
                "КПП": "tax|kpp",
                # "Дата постановки на учет": [],
                "Наименование налогового органа": "tax|service_name",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            "Сведения о регистрации в качестве страхователя в территориальном "\
            "органе Пенсионного фонда Российской Федерации": {
                "Регистрационный номер": "pfr|reg_num",
                # "Дата регистрации": [],
                "Наименование территориального органа Пенсионного фонда":
                    "pfr|service_name",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            "Сведения о регистрации в качестве страхователя в исполнительном "\
            "органе Фонда социального страхования Российской Федерации": {
                "Регистрационный номер": "fss|reg_num",
                # "Дата регистрации": [],
                "Наименование исполнительного органа Фонда социального "\
                "страхования": "fss|service_name",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]]
            },
            # "Сведения об уставном капитале (складочном капитале, уставном фонде, "\
            # "паевых взносах)": {
            #    "Вид": [],
            #    "Размер (в рублях)": [],
            #    "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
            #    "сведения": [["grn", "date"], ["STRING", "DATE"]]
            # },
            "Сведения о лице, имеющем право без доверенности действовать от имени "\
            "юридического лица": {
                "Фамилия": "head|surname",
                "Имя": "head|name",
                "Отчество": "head|patronymic",
                "ИНН": "head|inn",
                # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                # "сведения": [["grn", "date"], ["STRING", "DATE"]],
                "Должность": "head|appointment",
            },
            # "Сведения об учредителях (участниках) юридического лица": {
            #    "Фамилия": [],
            #    "Имя": [],
            #    "Отчество": [],
            #    "ИНН": [],
            #    "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
            #    "сведения": [["grn", "date"], ["STRING", "DATE"]],
            #    "Номинальная стоимость доли (в рублях)": [],
            #    "Размер доли (в процентах)": [],
            #    "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
            #    "сведения": [["grn", "date"], ["STRING", "DATE"]]
            # },
            "Сведения о видах экономической деятельности по Общероссийскому "\
            "классификатору видов экономической деятельности "\
            "(ОКВЭД ОК 029-2001 КДЕС. Ред. 1)": {
                "Сведения об основном виде деятельности": {
                    "Код и наименование вида деятельности": "okved|main",
                    # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей указанные "\
                    # "сведения": [["grn", "date"], ["STRING", "DATE"]]
                },
                "Сведения о дополнительных видах деятельности": [
                    "okved|affix",
                    {
                        "Код и наименование вида деятельности": "item",
                        # "ГРН и дата внесения в ЕГРЮЛ записи, содержащей "\
                        # "указанные сведения": [["grn", "date"], ["STRING", "DATE"]]
                    }
                ]
            },
            "Сведения о записях, внесенных в Единый государственный реестр "\
            "юридических лиц": "STOP_TAG"
        }

        __EGRIP_SCHEMA__NALOG_RU_PDF = {

        }

        def __init__(self, entity_type):
            self.__stack = {
                "root": self.__EGRUL_SCHEMA__NALOG_RU_PDF.copy() if entity_type == "ul" else self.__EGRIP_SCHEMA__NALOG_RU_PDF.copy()
            }

            self.__indx = 0
            self.__top = self.__stack
            self.__list = None

        def __get_top(self):
            """Docstring"""
            return self.__get_lvl(self.__indx)

        def __get_lvl(self, indx):
            """Docstring"""
            return reduce(lambda d, k: d.get(k), ["node" for i in range(indx)], self.__stack)

        def __normalize(self):
            """Docstring"""
            if not self.__indx and len(self.__top["root"]) == 1:
                return False
            elif not self.__top["root"]:
                self.__indx -= 1
                self.__top = ""
                self.__top = self.__get_top()
                return self.__normalize()
            return True

        def push_data(self, key, val, dst):
            """Docstring"""
            if "node" in self.__top\
                    and isinstance(self.__top["node"], list)\
                    and key in self.__list:
                get_dict_val(dst, self.__top["node"][0])[-1][self.__list.pop(key)] = val
                return True
            elif key in self.__top["root"]\
                    and isinstance(self.__top["root"][key], basestring):
                set_dict_val(dst, self.__top["root"].pop(key), val)
                return self.__normalize()
            return True

        def push_sect(self, key, dst):
            """Docstring"""
            if "node" in self.__top\
                    and isinstance(self.__top["node"], list):
                self.__top["node"] = ""
                self.__list = None
                if not self.__normalize():
                    return False

            for i in range(self.__indx + 1)[::-1]:
                tmp_top = self.__get_lvl(i)

                if key in tmp_top["root"]:
                    if not i and tmp_top["root"][key] == "STOP_TAG":
                        return False
                    if isinstance(tmp_top["root"][key], dict):
                        tmp_top["node"] = {"root": tmp_top["root"].pop(key)}
                        self.__indx = i + 1
                        self.__top = self.__get_top()
                        return True
                    elif isinstance(tmp_top["root"][key], list):
                        tmp_top["node"] = tmp_top["root"].pop(key)
                        set_dict_val(dst, tmp_top["node"][0], [])
                        self.__indx = i
                        self.__top = self.__get_top()
                        return True
                    else:
                        continue
            return True

        def push_cell(self, dst):
            """Docstring"""
            if "node" in self.__top and isinstance(self.__top["node"], list):
                self.__list = self.__top["node"][1].copy()
                get_dict_val(dst, self.__top["node"][0]).append({})
            return True

    def __init__(self):
        self.__pdf_fname = None
        self.__row_parser = None

    def parse(self, pdf_fname, dst):
        """Docstring"""
        self.__pdf_fname = pdf_fname
        page_number = 1
        row_list_of_page = self.__list_extractor(page_number)
        entity_type = self.__get_entity_type(row_list_of_page[0][0])

        if not entity_type:
            return False

        dst["entity"] = entity_type

        self.__row_parser = self.RowParser(entity_type)
        row_list_of_page = row_list_of_page[self.__NUM_OF_HDR_LINES_HDR_PAGE:]

        while self.__parse_page(row_list_of_page, dst):
            page_number += 1
            row_list_of_page = self.__list_extractor(page_number)
        return True

    def __get_entity_type(self, header):
        """Docstring"""
        match = re.search(r"|".join(self.__ENTITY_TYPE__NALOG_RU_PDF.keys()),
                          header)
        if match:
            cur_node = self.__ENTITY_TYPE__NALOG_RU_PDF[match.group(0)]
            if isinstance(cur_node, dict):
                match = re.search(r"|".join(cur_node.keys()), header)
                if match:
                    return cur_node[match.group(0)]
                return False
            else:
                return cur_node
        return False

    def __list_extractor(self, page_number):
        """Docstring"""
        cells = pdf.process_page(self.__pdf_fname, str(page_number))
        cells = [item for item in cells]
        return pdf.table_to_list(
            cells,
            [str(page_number)])[page_number][:-self.__NUM_OF_FTR_LINES]

    def __parse_page(self, row_list, dst):
        """Docstring"""
        for row in row_list:
            if row[0]:
                if row[0].isdigit():
                    if row[1]:
                        if not self.__row_parser.push_data(row[1], row[2], dst):
                            return False
                    else:
                        if not self.__row_parser.push_cell(dst):
                            return False
                else:
                    if not self.__row_parser.push_sect(row[0], dst):
                        return False
        return True



enrp = EgrulNalogRuPdf()
dst = {}
if enrp.parse("example.pdf", dst):
    pp.pprint(dst)
else:
    print "FAIL"
