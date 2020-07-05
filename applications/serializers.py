from rest_framework import serializers

from accounts.serializers import ProfilePageSerializer, UserSimpleSerializerVerTwo
from applications.models import TeamApplication, JoinQuestion, JoinAnswer
from teams.serializers import TeamSerializer


# 신청 create 할 때 직무/질문 만 들어올 듯
# 신청 list 뽑을 때는 팀 정보, 팀 신청 정보 있으면 될거야
# 신청 update : 변경할 수 있는것은 질문에 대한 대답과 직무!
class TeamApplicationSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True)  # read_only=True :: id 만 전달해도 되나 ?
    # 질문/대답도 같이 반환해야 하는데!
    applicant = UserSimpleSerializerVerTwo(read_only=True)

    class Meta:
        model = TeamApplication
        fields = ['id', 'applicant', 'join_status', 'job', 'created_at']  # 'team',
        read_only_fields = ['id', 'applicant', 'join_status', 'created_at']  # 'team', 이렇게 하면 team 빠지나 ? oo

    def update(self, instance, validated_data):
        instance.job = validated_data.get('job', instance.job)

        # 나중에 질문도 수정해야한다!

        return instance
    # def validate(self, attrs):
    #     print(type(attrs))
    #     print(attrs.values())
    #     return attrs


# class JoinQuestionListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         questions = [JoinQuestion(**item) for item in validated_data]
#         return JoinQuestion.objects.bulk_create(questions)


class JoinQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinQuestion
        fields = ['id', 'question']
        # read_only_fields = ['id','team']
        # list_serializer_class = JoinQuestionListSerializer

    # def to_internal_value(self, data): # dict to python
    #     print("to_internal_value",data)
    #
    #     super().to_internal_value(data)


class JoinAnswerSerializer(serializers.ModelSerializer):
    # question = serializers.CharField(read_only=True)

    class Meta:
        model = JoinAnswer
        fields = ['answer', 'question']  # 'question',


class TeamApplicationListSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True)  # read_only=True :: id 만 전달해도 되나 ?
    # 질문/대답도 같이 반환해야 하는데!
    applicant = UserSimpleSerializerVerTwo(read_only=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = TeamApplication
        fields = ['id', 'applicant', 'join_status', 'job', 'created_at', 'answers']  # 'team',
        read_only_fields = ['id', 'applicant', 'join_status', 'created_at']  # 'team', 이렇게 하면 team 빠지나 ? oo

    def get_answers(self, obj):
        # result = []
        serializer = JoinAnswerSerializer(instance=obj.answers.all(), many=True)
        print('get_answers', serializer.data)#obj.answers.all())
        return serializer.data
