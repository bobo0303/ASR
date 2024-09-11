from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Any

# [AbstractModel]


class AbstractModel(BaseModel):
    uid: str
    create_time: str
    lm_time: str
    lm_user: str


# [BaseResponse]
class Status:
    OK = "OK"
    FAILED = "FAILED"


R = TypeVar("R")


class BaseResponse(GenericModel, Generic[R]):

    status: str = Status.OK
    message: str = ""
    data: R


class CreateSuccessResponse(BaseResponse[str]):
    """
    新增資料成功response
    """
    data = "create data success."


class UpdateSuccessResponse(BaseResponse[str]):
    """
    更新資料成功response
    """
    data = "update data success."


class DeleteSuccessResponse(BaseResponse[str]):
    """
    刪除資料成功response
    """
    data = "delete data success."

# [ModelInitialization]


class ModelInitialization():

    @classmethod
    def init(cls, data: Any):
        """
        將data source table轉成data object

        args:
            data: data source
        """
        columns = list(cls.schema().get("properties").keys())
        result = {}
        for c in columns:
            if hasattr(data, c):
                val = getattr(data, c)
                result[c] = val
        cls.customized(cls, result=result, data=data)
        return result

    @classmethod
    def init_list(cls, data_list: list):
        """
        將data source table list轉成data object list

        args:
            data_list: data source list
        """
        result_list = []
        for data in data_list:
            result_list.append(cls.init(data=data))
        return result_list

    def customized(cls, result: dict, data: Any):
        pass