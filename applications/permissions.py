from rest_framework.permissions import BasePermission


class IsTeamLeader(BasePermission):
    # 사실 get_object 하면 호출되는 로직인데 list 에서는 안하잖아?
    # 이거 해보고 형선오빠 어떻게 했는지 확인해보기
    # 나는 먹힐리가 없다고 생각하긴하는데...! - get_object 할 때는 적용되겠지
    # 그래서 기존에 있던거랑 같이 사용했구나...!
    def has_object_permission(self, request, view, obj):  # Team
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.author  # False 로 놓고도 테스트해보기


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj): # TeamApplication
        # ?? 뷰에서 팀 리더인지 어떻게 알지 ?
        # api 요청한 사용자의 이메일이 팀 리더의 이메일과 같다면 True 반환 해서 확인하려고 했지!
        return request.user.email == obj.applicant.email


class IsApplicationTeamLeader(BasePermission):
    def has_object_permission(self, request, view, obj): # TeamApplication
        return request.user.email == obj.team.author.email
