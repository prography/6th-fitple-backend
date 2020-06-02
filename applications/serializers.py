from rest_framework import serializers

from accounts.serializers import ProfilePageSerializer, UserSimpleSerializer
from applications.models import TeamApplication
from teams.serializers import TeamSerializer


# 신청 create 할 때 직무/질문 만 들어올 듯
# 신청 list 뽑을 때는 팀 정보, 팀 신청 정보 있으면 될거야
# 신청 update : 변경할 수 있는것은 질문에 대한 대답과 직무!
class TeamApplicationSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True)  # read_only=True :: id 만 전달해도 되나 ?
    # 질문/대답도 같이 반환해야 하는데!
    applicant = UserSimpleSerializer(read_only=True)
    # applicant_name = serializers.
    # applicant_id = #ProfilePageSerializer()#UserSerializer#serializers.CharField() # 또
    # 다시 정보 요청을 위해 id 는 반드시 있어야할거같은데, 시리얼라이저를 새로 만들까 고민
    # id 랑 Username 만 있는 ? -- 다른거 더 필요한거 있을까 ? 신청정보 볼 때 user 정보도 한꺼번에 보길 원할까 ? 물어보기
    # 이미지도 있어야지.. 만드는게 낫겠다!

    class Meta:
        model = TeamApplication
        fields = ['id','applicant', 'join_status', 'job', 'created_at']#'team',
        read_only_fields = ['id','applicant', 'join_status', 'created_at']#'team', 이렇게 하면 team 빠지나 ? oo

    def update(self, instance, validated_data):
        instance.job = validated_data.get('job', instance.job)

        # 나중에 질문도 수정해야한다!

        return instance
    # def validate(self, attrs):
    #     print(type(attrs))
    #     print(attrs.values())
    #     return attrs
