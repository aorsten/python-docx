# encoding: utf-8

"""
Custom element classes related to the numbering part
"""

from . import OxmlElement
from .shared import CT_DecimalNumber, CT_String
from .simpletypes import ST_DecimalNumber
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne
)

class CT_AbstractNum(BaseOxmlElement):
    """
    ``<w:abstractNum>`` element
    """
    nsid = OneAndOnlyOne('w:nsid')
    multiLevelType = OneAndOnlyOne('w:multiLevelType')
    lvl = ZeroOrMore('w:lvl')
    abstractNumId = RequiredAttribute('w:abstractNumId', ST_DecimalNumber)

#     def add_lvl(self, ilvl):
#         """
#         Return a newly added CT_NumLvl (<w:lvlOverride>) element having its
#         ``ilvl`` attribute set to *ilvl*.
#         """
#         return self._add_lvl(ilvl=ilvl)
#     
#     @classmethod
#     def new(cls, abstract_num_id, nsid, multiLevelType):
#         abstractNum = OxmlElement('w:abstractNum')
#         abstractNum.abstractNumId = abstract_num_id
#           
#         #: Add nsid
#         nsid = CT_String.new(
#             'w:nsid', nsid
#         )
#         abstractNum.append(nsid)
#           
#         #: Add multiLevelType
#         multiLevelType = CT_String.new(
#             'w:multiLevelType', multiLevelType
#         )
#         abstractNum.append(multiLevelType)
#             
#           
#         return abstractNum

class CT_Num(BaseOxmlElement):
    """
    ``<w:num>`` element, which represents a concrete list definition
    instance, having a required child <w:abstractNumId> that references an
    abstract numbering definition that defines most of the formatting details.
    """
    abstractNumId = OneAndOnlyOne('w:abstractNumId')
    lvlOverride = ZeroOrMore('w:lvlOverride')
    numId = RequiredAttribute('w:numId', ST_DecimalNumber)

    def add_lvlOverride(self, ilvl, start, numFmt):
        """
        Return a newly added CT_NumLvl (<w:lvlOverride>) element having its
        ``ilvl`` attribute set to *ilvl*.
        """
        return self._add_lvlOverride(ilvl=ilvl, start=start, numFmt=numFmt)

    @classmethod
    def new(cls, num_id, abstractNum_id):
        """
        Return a new ``<w:num>`` element having numId of *num_id* and having
        a ``<w:abstractNumId>`` child with val attribute set to
        *abstractNum_id*.
        """
        num = OxmlElement('w:num')
        num.numId = num_id
        abstractNumId = CT_DecimalNumber.new(
            'w:abstractNumId', abstractNum_id
        )
        num.append(abstractNumId)
        return num

class CT_AbstractNumLvl(BaseOxmlElement):
    """
    ``<w:lvl>`` element, which identifies a level in a list
    definition with settings it contains.
    """
    start = OneAndOnlyOne('w:start')
    numFmt = OneAndOnlyOne('w:numFmt')
    ilvl = RequiredAttribute('w:ilvl', ST_DecimalNumber)
    
#     def add_start(self, start, numFmt):
#         return self._add_lvl(start=start, numFmt=numFmt)
#     @classmethod
#     def new(cls, ilvl, start, numFmt):
#         """
#         Return a new ``<w:num>`` element having numId of *num_id* and having
#         a ``<w:abstractNumId>`` child with val attribute set to
#         *abstractNum_id*.
#         """
#         lvl = OxmlElement('w:lvl')
#         lvl.ilvl = ilvl
#         start = CT_DecimalNumber.new(
#             'w:start', start
#         )
#         lvl.append(start)
#         numFmt = CT_String.new(
#             'w:numFmt', numFmt
#         )
#         lvl.append(numFmt)
#         return lvl

class CT_NumLvl(BaseOxmlElement):
    """
    ``<w:lvlOverride>`` element, which identifies a level in a list
    definition to override with settings it contains.
    """
    startOverride = ZeroOrOne('w:startOverride', successors=('w:lvl',))
    ilvl = RequiredAttribute('w:ilvl', ST_DecimalNumber)

    def add_startOverride(self, val):
        """
        Return a newly added CT_DecimalNumber element having tagname
        ``w:startOverride`` and ``val`` attribute set to *val*.
        """
        return self._add_startOverride(val=val)


class CT_NumPr(BaseOxmlElement):
    """
    A ``<w:numPr>`` element, a container for numbering properties applied to
    a paragraph.
    """
    ilvl = ZeroOrOne('w:ilvl', successors=(
        'w:numId', 'w:numberingChange', 'w:ins'
    ))
    numId = ZeroOrOne('w:numId', successors=('w:numberingChange', 'w:ins'))

    # @ilvl.setter
    # def _set_ilvl(self, val):
    #     """
    #     Get or add a <w:ilvl> child and set its ``w:val`` attribute to *val*.
    #     """
    #     ilvl = self.get_or_add_ilvl()
    #     ilvl.val = val

    # @numId.setter
    # def numId(self, val):
    #     """
    #     Get or add a <w:numId> child and set its ``w:val`` attribute to
    #     *val*.
    #     """
    #     numId = self.get_or_add_numId()
    #     numId.val = val


class CT_Numbering(BaseOxmlElement):
    """
    ``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml
    """
    abstractNum = ZeroOrMore('w:abstractNum', successors=('w:num',))
    num = ZeroOrMore('w:num', successors=('w:numIdMacAtCleanup',))

    def add_num(self, abstractNum_id):
        """
        Return a newly added CT_Num (<w:num>) element referencing the
        abstract numbering definition identified by *abstractNum_id*.
        """
        next_num_id = self._next_numId
        num = CT_Num.new(next_num_id, abstractNum_id)
        return self._insert_num(num)

#     def add_abstractNum(self, nsid, multiLevelType):
#         """
#         Return a newly added CT_AbstractNum (<w:num>) element referencing the
#         abstract numbering definition identified by *abstractNum_id*.
#         """
#         next_abstract_num_id = self._next_abstractNumId
#         abstractNum = CT_AbstractNum.new(next_abstract_num_id, nsid, multiLevelType)
#         return self._insert_abstractNum(abstractNum)

    def num_having_numId(self, numId):
        """
        Return the ``<w:num>`` child element having ``numId`` attribute
        matching *numId*.
        """
        xpath = './w:num[@w:numId="%d"]' % numId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            raise KeyError('no <w:num> element with numId %d' % numId)

    @property
    def _next_numId(self):
        """
        The first ``numId`` unused by a ``<w:num>`` element, starting at
        1 and filling any gaps in numbering between existing ``<w:num>``
        elements.
        """
        numId_strs = self.xpath('./w:num/@w:numId')
        num_ids = [int(numId_str) for numId_str in numId_strs]
        for num in range(1, len(num_ids)+2):
            if num not in num_ids:
                break
        return num
#     @property
#     def _next_abstractNumId(self):
#         numId_strs = self.xpath('./w:abstractNum/@w:abstractNumId')
#         num_ids = [int(numId_str) for numId_str in numId_strs]
#         for num in range(1, len(num_ids)+2):
#             if num not in num_ids:
#                 break
#         return num
