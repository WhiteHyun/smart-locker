
class makeQuery:

    def __init__(self) -> None:
        pass

    def dict2Query(tableNm,dict):
        """
        딕셔너리 자료형을 INSERT 문으로 변환
        tableNm : insert 할 Table
        dict : 딕셔너리
        """

        sQuery = "INSERT INTO "
        sQuery += tableNm
        
        sField = "("
        sValue = " VALUES(" 

        first = True
        for key,value in dict.items():
            
            if sValue == None:
                continue
            if first:
                first = False
            else:
                sField +=', '
                sValue +=', '
                
            sValue += f"\'{value}\'"
                
            sField += key

        sField += ") "
        sValue +=") "

        sQuery += sField
        sQuery += sValue

        return sQuery

