from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.champion import ChampionStatusData, ChampionStatusListData
from ..dto.champion import ChampionDto, ChampionListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(ChampionDto, ChampionStatusData)
    def champion_dto_to_data(self, value: ChampionDto, context: PipelineContext = None) -> ChampionStatusData:
        data = deepcopy(value)
        return ChampionStatusData.from_dto(data)

    @transform.register(ChampionListDto, ChampionStatusListData)
    def champion_list_dto_to_data(self, value: ChampionListDto, context: PipelineContext = None) -> ChampionStatusListData:
        data = deepcopy(value)
        data["champions"] = [self.champion_dto_to_data(c) for c in data["champions"]]
        for c in data["champions"]:
            c._update({"region": data["region"]})
        data = data["champions"]
        return ChampionStatusListData(data)
