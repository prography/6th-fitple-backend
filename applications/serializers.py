from rest_framework import serializers

from accounts.serializers import ProfilePageSerializer, UserSimpleSerializer
from applications.models import TeamApplication, JoinQuestions, JoinAnswers
from teams.serializers import TeamSerializer


# 신청 create 할 때 직무/질문 만 들어올 듯
# 신청 list 뽑을 때는 팀 정보, 팀 신청 정보 있으면 될거야
# 신청 update : 변경할 수 있는것은 질문에 대한 대답과 직무!
class TeamApplicationSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True)  # read_only=True :: id 만 전달해도 되나 ?
    # 질문/대답도 같이 반환해야 하는데!
    applicant = UserSimpleSerializer(read_only=True)

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


class JoinQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinQuestions
        fields = ['question1', 'question2', 'question3']

    # def to_internal_value(self, data): # dict to python
    #     print("to_internal_value",data)
    #
    #     super().to_internal_value(data)


class JoinAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinAnswers
        fields = ['answer1', 'answer2', 'answer3']

    def to_internal_value(self, data): # dict to python
        print("to_internal_value",data)

        # print("data[0]",data[0])
        input_data = {'answer1': data[0], 'answer2': data[1], 'answer3': data[2]}
        return input_data
        # print(input_data)
        # super().to_internal_value(input_data)

        # super().to_internal_value(data)
        # input_data = {'answer1': data[0], 'answer2': data[1], 'answer3': data[2]}

