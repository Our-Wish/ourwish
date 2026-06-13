"""drf-spectacular 확장.

커스텀 인증 클래스(MemberJWTAuthentication)를 OpenAPI 문서에 'JWT Bearer'로
표시하기 위한 확장. 이 모듈이 임포트되면 drf-spectacular가 자동 등록한다.
(AccountsConfig.ready()에서 임포트)
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class MemberJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "apps.accounts.authentication.MemberJWTAuthentication"
    name = "jwtAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
