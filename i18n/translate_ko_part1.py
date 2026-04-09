#!/usr/bin/env python3
"""Generate Korean translations for strings_chunk_1.json"""
import json

with open('/Users/fredericlumiere/apiant-website/i18n/strings_chunk_1.json', 'r') as f:
    strings = json.load(f)

translations = {}

for s in strings:
    # By default, keep the string as-is (for numbers, codes, symbols, brand names)
    translations[s] = s

# Now override with actual Korean translations
ko = {
    "\"A chat is one trigger and one action. Everything between is up to your imagination.\"":
        "\"채팅은 하나의 트리거와 하나의 액션입니다. 그 사이의 모든 것은 여러분의 상상력에 달려 있습니다.\"",
    "\"A chatbot is one trigger and one action. Everything between is up to your imagination.\"":
        "\"챗봇은 하나의 트리거와 하나의 액션입니다. 그 사이의 모든 것은 여러분의 상상력에 달려 있습니다.\"",
    "\"A contact update comes into HubSpot. The master account receives the webhook, identifies which MindBody site the contact belongs to based on the location field, and routes the update to the correct child account. The child account processes it through its own automation with its own MindBody credentials. The contact never knows there are 228 locations behind the scenes.\"":
        "\"연락처 업데이트가 HubSpot으로 들어옵니다. 마스터 계정이 webhook을 수신하고, 위치 필드를 기반으로 해당 연락처가 어느 MindBody 사이트에 속하는지 식별한 후, 올바른 하위 계정으로 업데이트를 라우팅합니다. 하위 계정은 자체 MindBody 자격 증명으로 자체 자동화를 통해 처리합니다. 연락처는 뒤에 228개의 지점이 있다는 사실을 전혀 알지 못합니다.\"",
    "\"APIANT has proven to be an invaluable asset for our organization. Robust integration solutions.\"":
        "\"APIANT는 저희 조직에 없어서는 안 될 귀중한 자산임이 입증되었습니다. 강력한 통합 솔루션입니다.\"",
    "\"An amazing partner! Has allowed us to develop a comprehensive integration solution.\"":
        "\"놀라운 파트너! 포괄적인 통합 솔루션을 개발할 수 있게 해주었습니다.\"",
    "\"Awesomesauce! If you're looking to deliver exceptional results and drive innovation, look no further.\"":
        "\"정말 훌륭합니다! 탁월한 결과를 제공하고 혁신을 추진하고 싶다면, 더 찾아볼 필요가 없습니다.\"",
    "\"Code Sync\" Dropdowns": "\"Code Sync\" 드롭다운",
    "\"CodeSync\" for Dropdowns": "드롭다운용 \"CodeSync\"",
    "\"Execute an automation workflow\"": "\"자동화 워크플로우 실행\"",
    "\"Fast Theme Changes in Blured have transformed the way I work. Switching between themes on-the-fly helps me align my coding environment with different project requirements swiftly. Glossy has truly streamlined my workflow.\"":
        "\"Blured의 빠른 테마 변경 기능이 제 작업 방식을 완전히 바꿔놓았습니다. 테마를 즉시 전환할 수 있어 코딩 환경을 다양한 프로젝트 요구사항에 신속하게 맞출 수 있습니다. Glossy는 정말로 제 워크플로우를 간소화했습니다.\"",
    "\"Fast Theme Changes in Blured have transformed the way I work.\"":
        "\"Blured의 빠른 테마 변경 기능이 제 작업 방식을 완전히 바꿔놓았습니다.\"",
    "\"Great Partners! We've been partnering with Apiant since 2019. THANK YOU!\"":
        "\"훌륭한 파트너! 2019년부터 Apiant과 파트너십을 맺어왔습니다. 감사합니다!\"",
    "\"Great partnership. We are very happy to continue working together with Apiant !\"":
        "\"훌륭한 파트너십입니다. Apiant과 계속 함께 일하게 되어 매우 기쁩니다!\"",
    "\"List active API connections\"": "\"활성 API 연결 목록 조회\"",
    "\"Longtime customer and a huge fan! Absolutely crucial for my biz. Couldn't do it without Apiant.\"":
        "\"오랜 고객이자 열렬한 팬입니다! 제 비즈니스에 절대적으로 중요합니다. Apiant 없이는 할 수 없었습니다.\"",
    "\"Nothing We Have Seen Comes Close To The Power And Versatility Of The APIANT Platform.\"":
        "\"APIANT 플랫폼의 성능과 다재다능함에 비견할 수 있는 것을 본 적이 없습니다.\"",
    "\"Powerful Automation, Bespoke Solutions.\"":
        "\"강력한 자동화, 맞춤형 솔루션.\"",
    "\"Professional Team and Excellent Experience. A company that will work with you and for you.\"":
        "\"전문적인 팀과 탁월한 경험. 여러분과 함께, 여러분을 위해 일하는 회사입니다.\"",
    "\"Query connected system data\"": "\"연결된 시스템 데이터 조회\"",
    "\"Real data, real APIs, real business logic. Not sandboxed demos.\"":
        "\"실제 데이터, 실제 API, 실제 비즈니스 로직. 샌드박스 데모가 아닙니다.\"",
    "\"Seamless Implementation and Expert Support! Reliable and effective automation solutions.\"":
        "\"원활한 구현과 전문적인 지원! 신뢰할 수 있고 효과적인 자동화 솔루션입니다.\"",
    "\"Seamless Integrations - Professional Service. Has been instrumental in integrating our data factory across more than 200 locations.\"":
        "\"원활한 통합 - 전문적인 서비스. 200개 이상의 지점에 걸쳐 데이터 팩토리를 통합하는 데 핵심적인 역할을 했습니다.\"",
    "\"The Assembly Editor is where API endpoints become reusable building blocks -- what we call ingredients. Traditionally, this is where builders either accelerate or stall. The ones who master it become unstoppable. The AI Co-Pilot eliminates the learning curve entirely.\"":
        "\"Assembly Editor는 API 엔드포인트가 재사용 가능한 빌딩 블록(우리가 ingredient라고 부르는 것)이 되는 곳입니다. 전통적으로 이 단계에서 빌더들은 가속하거나 정체합니다. 이를 마스터한 사람은 막을 수 없게 됩니다. AI Co-Pilot이 학습 곡선을 완전히 제거합니다.\"",
    "\"The Deep Integration Gap\"": "\"깊은 통합 격차\"",
    "\"The Deep Integration Gap: Bridging the Divide Between Open APIs and Business Needs\"":
        "\"깊은 통합 격차: 개방형 API와 비즈니스 요구 사이의 간극 해소\"",
    "\"The Preeminent Integration & Automation: Everything-You-Could-Ever-Need Platform.\"":
        "\"최고의 통합 및 자동화: 필요한 모든 것을 갖춘 플랫폼.\"",
    "\"The same automation that serves a single-location yoga studio also serves a 228-location franchise. The logic is identical. The settings are different.\"":
        "\"단일 지점 요가 스튜디오를 서비스하는 동일한 자동화가 228개 지점 프랜차이즈도 서비스합니다. 로직은 동일합니다. 설정만 다릅니다.\"",
    "\"This Is My Bet On Who Wins The API Economy. Incredibly flexible and easy to understand.\"":
        "\"이것이 API 경제의 승자에 대한 제 예측입니다. 믿을 수 없을 만큼 유연하고 이해하기 쉽습니다.\"",
    "\"jane@acme.com\"": "\"jane@acme.com\"",
    "\"sync-contact-to-hubspot\"": "\"sync-contact-to-hubspot\"",
    "$$$ to build": "구축에 $$$",
    "(string, required)": "(string, 필수)",
    "+ additional usage": "+ 추가 사용량",
    ", and": ", 그리고",
    ", or let the": ", 또는",
    "-- complete integrations with logic, branching, and error handling.":
        "-- 로직, 분기, 오류 처리가 포함된 완전한 통합.",
    "-- individual API operations like \"Get Client Services by Product ID\" or \"Delete Task in Asana.\" These ingredients are then combined in the Automation Editor into":
        "-- \"제품 ID로 고객 서비스 가져오기\" 또는 \"Asana에서 작업 삭제\"와 같은 개별 API 작업. 이 ingredient들은 Automation Editor에서 결합되어",
    ". The AI Co-Pilot eliminates the learning curve entirely. Type the name of any app. The Co-Pilot finds the API documentation, determines authentication, builds connectors, tests them against live APIs, and self-corrects when something breaks.":
        ". AI Co-Pilot이 학습 곡선을 완전히 제거합니다. 앱 이름을 입력하면 Co-Pilot이 API 문서를 찾고, 인증 방식을 결정하고, 커넥터를 구축하고, 실제 API에 대해 테스트하고, 문제가 발생하면 자체 수정합니다.",
    ". They build visually, use the AI Co-Pilot for new API connections, and the platform handles rate limiting, error handling, retry logic, monitoring, and scaling.":
        ". 시각적으로 구축하고, 새로운 API 연결에 AI Co-Pilot을 사용하며, 플랫폼이 속도 제한, 오류 처리, 재시도 로직, 모니터링, 확장을 처리합니다.",
    ". Traditionally, this is where builders either accelerate or stall. The ones who master it become unstoppable. The AI Co-Pilot eliminates the learning curve entirely.":
        ". 전통적으로 이 단계에서 빌더들은 가속하거나 정체합니다. 이를 마스터한 사람은 막을 수 없게 됩니다. AI Co-Pilot이 학습 곡선을 완전히 제거합니다.",
    "/mo": "/월",
    "/month": "/월",
    "1 production server": "프로덕션 서버 1대",
    "1-Click": "1-Click",
    "100 customers at $99/mo": "고객 100명 × $99/월",
    "12 invoices": "인보이스 12건",
    "120+ Custom Client Properties": "120개 이상의 맞춤 고객 속성",
    "120+ Ready-Made Client Fields": "120개 이상의 기본 제공 고객 필드",
    "120+ custom properties": "120개 이상의 맞춤 속성",
    "140+ Custom Contact Fields": "140개 이상의 맞춤 연락처 필드",
    "140+ custom fields": "140개 이상의 맞춤 필드",
    "140+ donor properties": "140개 이상의 기부자 속성",
    "14:32:07 • GET /client/8847291/visits • 200 OK • 145ms": "14:32:07 • GET /client/8847291/visits • 200 OK • 145ms",
    "14:32:07 • MindBody webhook • 200 OK • 23ms": "14:32:07 • MindBody webhook • 200 OK • 23ms",
    "14:32:08 • Condition evaluated • True path taken": "14:32:08 • 조건 평가 완료 • True 경로 실행",
    "14:32:08 • PATCH /crm/v3/objects/appointments • 200 OK • 312ms": "14:32:08 • PATCH /crm/v3/objects/appointments • 200 OK • 312ms",
    "15-Minute Data Refresh": "15분 데이터 갱신",
    "17 Turnkey Products. Built on APIANT. Shipped to Thousands.": "17개 턴키 제품. APIANT 기반. 수천 곳에 제공.",
    "17 integration products": "17개 통합 제품",
    "2 dedicated AWS servers (prod + dev)": "전용 AWS 서버 2대 (프로덕션 + 개발)",
    "2-minute interactive demo · No signup required": "2분 인터랙티브 데모 · 가입 불필요",
    "20+ hrs": "20시간 이상",
    "228 Locations. One Platform. Zero Errors.": "228개 지점. 하나의 플랫폼. 오류 제로.",
    "228 child accounts total": "총 228개 하위 계정",
    "228 child accounts • 6 automations active": "228개 하위 계정 • 6개 자동화 활성",
    "228 of 228 selected": "228개 중 228개 선택됨",
    "250+ API Connectors": "250개 이상의 API 커넥터",
    "250+ API connectors": "250개 이상의 API 커넥터",
    "27 Prebuilt Connectors": "27개 사전 구축 커넥터",
    "27 prebuilt connectors": "27개 사전 구축 커넥터",
    "3 tickets": "티켓 3건",
    "360 Donor View in HubSpot": "HubSpot에서 기부자 360도 뷰",
    "360° Donor View in HubSpot": "HubSpot에서 기부자 360° 뷰",
    "47 emails": "이메일 47건",
    "5 (test only)": "5개 (테스트 전용)",
    "500 customers at $99/mo": "고객 500명 × $99/월",
    "500+ Connectors": "500개 이상의 커넥터",
    "500+ connectors, AI processing, conditional logic, data transformations, error handling, the full platform running invisibly behind the scenes.":
        "500개 이상의 커넥터, AI 처리, 조건부 로직, 데이터 변환, 오류 처리 등 전체 플랫폼이 보이지 않는 곳에서 실행됩니다.",
    "6 automations affected": "6개 자동화 영향받음",
    "76 active": "76개 활성",
    "99.99% SLA": "99.99% SLA",
    ": Per Customer": ": 고객별",
    ": Universal": ": 범용",
    "< 2 min": "< 2분",
    "< 30 min": "< 30분",
    "? Send us a message.": "? 메시지를 보내주세요.",
    "A \"payload\" is a single event or data transfer between Mindbody and Zapier (like a new client or booking update). Your monthly subscription includes 1,000 payloads, with additional payloads available at $0.04 each.":
        "\"payload\"는 Mindbody와 Zapier 간의 단일 이벤트 또는 데이터 전송(예: 신규 고객 또는 예약 업데이트)을 의미합니다. 월간 구독에는 1,000개의 payload가 포함되며, 추가 payload는 개당 $0.04에 이용할 수 있습니다.",
    "A CRM integration has a setting: \"Custom object appointments: Yes/No.\" The automation branches based on that choice. Same codebase handles both paths. When a franchise adds five new locations, those locations inherit the master settings but can be individually configured.":
        "CRM 통합에는 \"맞춤 오브젝트 예약: 예/아니오\" 설정이 있습니다. 자동화는 해당 선택에 따라 분기합니다. 동일한 코드베이스가 두 경로를 모두 처리합니다. 프랜차이즈가 5개의 신규 지점을 추가하면 해당 지점은 마스터 설정을 상속하지만 개별적으로 구성할 수 있습니다.",
    "A CRM integration supports custom objects for class bookings. Some customers want custom objects, some do not. In the settings, there is a checkbox: \"Custom object appointments: Yes/No.\" The automation logic branches based on that setting. Same codebase handles both. When a franchise adds five new locations, those locations inherit the master settings but can be individually configured.":
        "CRM 통합은 수업 예약을 위한 맞춤 오브젝트를 지원합니다. 일부 고객은 맞춤 오브젝트를 원하고, 일부는 원하지 않습니다. 설정에 \"맞춤 오브젝트 예약: 예/아니오\" 체크박스가 있습니다. 자동화 로직은 해당 설정에 따라 분기합니다. 동일한 코드베이스가 두 가지를 모두 처리합니다. 프랜차이즈가 5개의 신규 지점을 추가하면 해당 지점은 마스터 설정을 상속하지만 개별적으로 구성할 수 있습니다.",
    "A Chat. One Trigger. One Action. Infinite Possibilities.":
        "채팅. 하나의 트리거. 하나의 액션. 무한한 가능성.",
    "A Cliniko patient with no email that's synced with HubSpot will not have an email in HubSpot either.":
        "이메일이 없는 Cliniko 환자가 HubSpot과 동기화되면 HubSpot에도 이메일이 없습니다.",
    "A FormApp is a custom UI connected directly to the APIANT automation engine. The settings you configure in the Automation Editor surface directly in the FormApp, giving your end users a clean, branded configuration experience, without exposing any of the underlying platform complexity.":
        "FormApp은 APIANT 자동화 엔진에 직접 연결된 맞춤 UI입니다. Automation Editor에서 구성한 설정이 FormApp에 직접 표시되어, 기본 플랫폼의 복잡성을 노출하지 않으면서 최종 사용자에게 깔끔한 브랜드 구성 경험을 제공합니다.",
    "A Mindbody client with no email that's synced with HubSpot will not have an email in HubSpot either.":
        "이메일이 없는 Mindbody 고객이 HubSpot과 동기화되면 HubSpot에도 이메일이 없습니다.",
    "A SaaS company's franchise sales team needs deep Mindbody integrations to close six-figure headquarter deals. Their internal team built a basic integration (four inbound events, limited sync) but priorities shifted to AI features. The integration is now static.":
        "한 SaaS 회사의 프랜차이즈 영업팀은 6자리 본사 계약을 체결하기 위해 심층적인 Mindbody 통합이 필요합니다. 내부 팀이 기본 통합(4개 인바운드 이벤트, 제한된 동기화)을 구축했지만 우선순위가 AI 기능으로 전환되었습니다. 통합은 현재 정적 상태입니다.",
    "A WORLD FIRST IN INTEGRATION PLATFORMS": "통합 플랫폼 분야의 세계 최초",
    "A chat is one trigger and one action. Everything between is up to your imagination. One user message can trigger complex automations (data lookups, conditional branching, API calls, notifications) all invisible to the user.":
        "채팅은 하나의 트리거와 하나의 액션입니다. 그 사이의 모든 것은 여러분의 상상력에 달려 있습니다. 사용자의 한 마디 메시지가 복잡한 자동화(데이터 조회, 조건부 분기, API 호출, 알림)를 트리거할 수 있으며, 이 모든 것은 사용자에게 보이지 않습니다.",
    "A chatbot that looks up order status, checks inventory, creates support tickets, processes refunds, and escalates to humans when needed. All in one conversation.":
        "주문 상태를 조회하고, 재고를 확인하고, 지원 티켓을 생성하고, 환불을 처리하고, 필요 시 상담원에게 전달하는 챗봇. 모두 하나의 대화에서 이루어집니다.",
    "A chatbot that looks up order status, checks inventory, creates tickets, and escalates to humans, all in one conversation flow.":
        "주문 상태를 조회하고, 재고를 확인하고, 티켓을 생성하고, 상담원에게 전달하는 챗봇. 모두 하나의 대화 흐름에서 이루어집니다.",
    "A chatbot that monitors regulatory deadlines, checks if required documents are filed, verifies vendor certifications, and alerts the compliance team about upcoming requirements.":
        "규제 마감일을 모니터링하고, 필수 문서가 제출되었는지 확인하고, 공급업체 인증을 검증하고, 다가오는 요구사항에 대해 컴플라이언스 팀에 알리는 챗봇.",
    "A complete virtual fitness solution": "완전한 가상 피트니스 솔루션",
    "A connection is a set of credentials into one of your customer's accounts. For example, if you connect to a customer's HubSpot account, that counts as one connection. Each unique customer account you integrate with uses one connection.":
        "연결은 고객 계정 중 하나에 대한 자격 증명 세트입니다. 예를 들어 고객의 HubSpot 계정에 연결하면 그것이 하나의 연결로 계산됩니다. 통합하는 각 고유 고객 계정마다 하나의 연결을 사용합니다.",
    "A customer submits a Data Subject Access Request (DSAR) through your chatbot. The chatbot verifies their identity, queries every system that holds their data, compiles a structured report, and delivers it. What used to take your legal team 20+ hours of manual work happens in under two minutes.":
        "고객이 챗봇을 통해 정보주체 접근 요청(DSAR)을 제출합니다. 챗봇이 신원을 확인하고, 데이터를 보유한 모든 시스템을 조회하고, 구조화된 보고서를 작성하여 전달합니다. 법무팀이 20시간 이상 수작업으로 처리하던 일이 2분 이내에 완료됩니다.",
    "A detailed PDF report has been sent to jane.doe@example.com. You can also request data erasure. Would you like to proceed?":
        "상세 PDF 보고서가 jane.doe@example.com으로 전송되었습니다. 데이터 삭제를 요청할 수도 있습니다. 진행하시겠습니까?",
    "A fitness franchise needed to unify 228 MindBody locations into a single HubSpot instance: every client's home location, secondary visits, frequency, membership status, and upcoming appointments in one place.":
        "한 피트니스 프랜차이즈가 228개의 MindBody 지점을 하나의 HubSpot 인스턴스로 통합해야 했습니다. 모든 고객의 주요 지점, 부가 방문, 빈도, 멤버십 상태, 예정된 예약을 한 곳에서 관리합니다.",
    "A fitness franchise with 228 locations needs booking data, membership changes, and purchase history synced to a single HubSpot instance with custom objects, bi-directional updates, and rate limiting. A shallow integration creates 228 disconnected data streams. A deep integration understands that when a client cancels Tuesday's class, their \"next scheduled visit\" refreshes across the entire system. That's the difference between data you can act on and data that misleads you.":
        "228개 지점을 보유한 피트니스 프랜차이즈가 예약 데이터, 멤버십 변경, 구매 이력을 맞춤 오브젝트, 양방향 업데이트, 속도 제한과 함께 단일 HubSpot 인스턴스에 동기화해야 합니다. 얕은 통합은 228개의 단절된 데이터 스트림을 생성합니다. 깊은 통합은 고객이 화요일 수업을 취소하면 \"다음 예정 방문\"이 전체 시스템에서 갱신된다는 것을 이해합니다. 이것이 실행 가능한 데이터와 오해를 불러일으키는 데이터의 차이입니다.",
    "A master account routes all CRM data to the correct Mindbody site. Rate limiting holds at 185 API calls per 10 seconds, calibrated to never exceed CRM limits even when every location renews memberships on January 1st. The Splunk dashboard proves it: zero errors, zero rate limit violations. New locations go live in hours, not weeks.":
        "마스터 계정이 모든 CRM 데이터를 올바른 Mindbody 사이트로 라우팅합니다. 속도 제한은 10초당 185 API 호출로 유지되며, 모든 지점이 1월 1일에 멤버십을 갱신해도 CRM 한도를 절대 초과하지 않도록 보정되었습니다. Splunk 대시보드가 이를 입증합니다. 오류 제로, 속도 제한 위반 제로. 신규 지점은 몇 주가 아닌 몇 시간 만에 가동됩니다.",
    "A master account with 228 child accounts, each representing a location. New locations get added to the network and immediately inherit shared connections and settings. This is how The Exercise Coach manages MindBody integrations across their entire franchise -- from a single control plane.":
        "228개의 하위 계정을 가진 마스터 계정으로, 각각 하나의 지점을 나타냅니다. 신규 지점이 네트워크에 추가되면 즉시 공유 연결과 설정을 상속받습니다. 이것이 The Exercise Coach가 단일 제어판에서 전체 프랜차이즈의 MindBody 통합을 관리하는 방식입니다.",
    "A new client profile is automatically created in Mindbody upon the first booking.":
        "첫 예약 시 Mindbody에 새 고객 프로필이 자동으로 생성됩니다.",
    "A single chat interaction can trigger complex automation behind the scenes. A customer asks a question in natural language. The chatbot interprets intent, fires a trigger, and the platform executes the full workflow - pulling data from one system, transforming it, pushing it to another, and returning a response. All in one conversational turn.":
        "단일 채팅 상호작용으로 백그라운드에서 복잡한 자동화를 트리거할 수 있습니다. 고객이 자연어로 질문하면, 챗봇이 의도를 해석하고, 트리거를 실행하고, 플랫폼이 전체 워크플로우를 실행합니다. 한 시스템에서 데이터를 가져오고, 변환하고, 다른 시스템으로 전송하고, 응답을 반환합니다. 모두 하나의 대화 턴에서 이루어집니다.",
    "A unique placeholder email is created in Zoho CRM, ensuring seamless syncing without interruptions.":
        "Zoho CRM에 고유한 임시 이메일이 생성되어 중단 없이 원활한 동기화를 보장합니다.",
    "A yoga studio member books Saturday morning yoga for the rest of the year. A shallow integration creates 52 records and calls it done. A deep integration understands that when the member attends Saturday's class, the \"next scheduled visit\" refreshes to next Saturday. When they cancel, it refreshes again. Getting that right is the difference between marketing automation that works and marketing automation that embarrasses you.":
        "요가 스튜디오 회원이 연말까지 토요일 아침 요가를 예약합니다. 얕은 통합은 52개 레코드를 생성하고 끝냅니다. 깊은 통합은 회원이 토요일 수업에 참석하면 \"다음 예정 방문\"이 다음 토요일로 갱신된다는 것을 이해합니다. 취소하면 다시 갱신됩니다. 이것을 올바르게 처리하는 것이 작동하는 마케팅 자동화와 실망스러운 마케팅 자동화의 차이입니다.",
    "AI Agent architecture showing goals, reasoning, and tool access to connectors, automations, business logic, and data queries":
        "목표, 추론, 커넥터/자동화/비즈니스 로직/데이터 조회에 대한 도구 접근을 보여주는 AI Agent 아키텍처",
    "AI Agent orchestrating a multi-step workflow with platform tools":
        "플랫폼 도구로 다단계 워크플로우를 조율하는 AI Agent",
    "AI Agents": "AI Agents",
    "AI Agents + Business Systems": "AI Agents + 비즈니스 시스템",
    "AI Agents That Operate Inside the Full Platform": "전체 플랫폼 내에서 운영되는 AI Agents",
    "AI Capabilities": "AI 기능",
    "AI Capabilities | AI That Acts - Not Just Answers": "AI 기능 | 답변만 하지 않고 행동하는 AI",
    "AI Chatbot": "AI Chatbot",
    "AI Chatbot Builder | Chatbots That Act on Real Data | APIANT": "AI Chatbot Builder | 실제 데이터로 행동하는 챗봇 | APIANT",
    "AI Co-Pilot": "AI Co-Pilot",
    "AI Co-Pilot building a Stripe connector: finds API docs, configures auth, builds 247 endpoints, tests them, and reveals available actions":
        "Stripe 커넥터를 구축하는 AI Co-Pilot: API 문서 검색, 인증 구성, 247개 엔드포인트 구축, 테스트, 사용 가능한 액션 표시",
    "AI Co-Pilot building an Asana connector in real time":
        "실시간으로 Asana 커넥터를 구축하는 AI Co-Pilot",
    "AI Co-Pilot builds it autonomously": "AI Co-Pilot이 자율적으로 구축합니다",
    "AI Co-Pilot builds it autonomously, overnight": "AI Co-Pilot이 밤새 자율적으로 구축합니다",
    "AI Co-Pilot for building": "구축을 위한 AI Co-Pilot",
    "AI Co-Pilot processing steps: reading API docs, building endpoints, testing against live APIs, and self-correcting auth methods":
        "AI Co-Pilot 처리 단계: API 문서 읽기, 엔드포인트 구축, 실제 API 대상 테스트, 인증 방법 자체 수정",
    "AI Co-Pilot, AI Agents with goals and tools, AI Chatbot":
        "AI Co-Pilot, 목표와 도구를 가진 AI Agents, AI Chatbot",
    "AI Co-Pilot: Building Asana \"Delete Task\"": "AI Co-Pilot: Asana \"작업 삭제\" 구축",
    "AI That Acts, Not Just Answers": "답변만 하지 않고 행동하는 AI",
    "AI That Doesn't Just Chat. AI That Acts.": "단순히 대화만 하지 않는 AI. 행동하는 AI.",
    "AI agents, chatbots, and LLM applications connect to 500+ integrations through MCP's open standard protocol.":
        "AI agents, 챗봇, LLM 애플리케이션이 MCP의 개방형 표준 프로토콜을 통해 500개 이상의 통합에 연결됩니다.",
    "AI capabilities": "AI 기능",
    "AI finds and reads the API documentation": "AI가 API 문서를 찾아서 읽습니다",
    "AI form": "AI 양식",
    "AI models connecting to APIANT via MCP protocol": "MCP 프로토콜을 통해 APIANT에 연결하는 AI 모델",
    "AI parses the request, identifies it as a GDPR DSAR, and validates the email against your CRM":
        "AI가 요청을 분석하고, GDPR DSAR로 식별하고, CRM과 대조하여 이메일을 검증합니다",
    "AI processing and intent detection": "AI 처리 및 의도 감지",
    "AI processing and reasoning": "AI 처리 및 추론",
    "AI systems that monitor, respond to, and act on events across your entire integration infrastructure.":
        "전체 통합 인프라에서 이벤트를 모니터링하고, 응답하고, 조치하는 AI 시스템.",
    "AI that operates inside the full integration platform. Not bolted-on. Not sandboxed. Production-ready.":
        "전체 통합 플랫폼 내에서 운영되는 AI. 단순 부착이 아닙니다. 샌드박스가 아닙니다. 프로덕션 준비 완료.",
    "AI-Accelerated Development": "AI 가속 개발",
    "AI-Powered": "AI 기반",
    "AI-Powered Fields": "AI 기반 필드",
    "AI-Powered Intake Forms": "AI 기반 접수 양식",
    "AI-Powered Workflows": "AI 기반 워크플로우",
    "AI-assisted connector building for any API": "모든 API를 위한 AI 지원 커넥터 구축",
    "API Apps": "API Apps",
    "API Apps aren't just connectors - they're powerful, expert-built solutions that seamlessly integrate Cliniko with the tools you rely on. Designed to handle complex workflows with precision, they drive efficiency, unlock new opportunities, and fuel business growth.":
        "API Apps는 단순한 커넥터가 아닙니다. Cliniko를 의존하는 도구와 원활하게 통합하는 전문가가 구축한 강력한 솔루션입니다. 복잡한 워크플로우를 정밀하게 처리하도록 설계되어, 효율성을 높이고, 새로운 기회를 열고, 비즈니스 성장을 촉진합니다.",
    "API Apps aren't just connectors - they're powerful, expert-built solutions that seamlessly integrate DonorPerfect with the tools you rely on. Designed to handle complex workflows with precision, they drive efficiency, unlock new opportunities, and fuel business growth.":
        "API Apps는 단순한 커넥터가 아닙니다. DonorPerfect를 의존하는 도구와 원활하게 통합하는 전문가가 구축한 강력한 솔루션입니다. 복잡한 워크플로우를 정밀하게 처리하도록 설계되어, 효율성을 높이고, 새로운 기회를 열고, 비즈니스 성장을 촉진합니다.",
    "API Apps aren't just connectors - they're powerful, expert-built solutions that seamlessly integrate Mindbody with the tools you rely on. Designed to handle complex workflows with precision, they drive efficiency, unlock new opportunities, and fuel business growth.":
        "API Apps는 단순한 커넥터가 아닙니다. Mindbody를 의존하는 도구와 원활하게 통합하는 전문가가 구축한 강력한 솔루션입니다. 복잡한 워크플로우를 정밀하게 처리하도록 설계되어, 효율성을 높이고, 새로운 기회를 열고, 비즈니스 성장을 촉진합니다.",
    "API Key": "API Key",
    "API calls managed per 10 sec": "10초당 관리되는 API 호출",
    "API calls per": "API 호출 /",
    "API calls per 10 seconds, enforced platform-wide": "10초당 API 호출, 플랫폼 전체에서 적용",
    "API calls to connected systems": "연결된 시스템으로의 API 호출",
    "API calls/10s": "API 호출/10초",
    "API documentation discovery": "API 문서 탐색",
    "APIANT (Dedicated Server)": "APIANT (전용 서버)",
    "APIANT AI Stack: AI Co-Pilot, AI Agents, AI Chatbot, and MCP Servers layers on the Integration Platform foundation":
        "APIANT AI 스택: 통합 플랫폼 기반 위의 AI Co-Pilot, AI Agents, AI Chatbot, MCP Servers 계층",
    "APIANT Admin Console showing per-customer settings panel with toggles driving automation logic branching":
        "고객별 설정 패널에서 토글로 자동화 로직 분기를 제어하는 APIANT Admin Console",
    "APIANT Automation Editor showing a Mindbody to HubSpot CRM sync flow with search, conditional branching, and data transformations":
        "검색, 조건부 분기, 데이터 변환이 포함된 Mindbody에서 HubSpot CRM으로의 동기화 흐름을 보여주는 APIANT Automation Editor",
    "APIANT Automation Editor showing a real Mindbody to HubSpot integration flow with conditional branching and 123 actions":
        "조건부 분기와 123개 액션이 포함된 실제 Mindbody에서 HubSpot으로의 통합 흐름을 보여주는 APIANT Automation Editor",
    "APIANT Automation Editor showing a real Mindbody to HubSpot integration flow with conditional branching, data transformations, and 123 actions":
        "조건부 분기, 데이터 변환, 123개 액션이 포함된 실제 Mindbody에서 HubSpot으로의 통합 흐름을 보여주는 APIANT Automation Editor",
    "APIANT Automation Engine": "APIANT Automation Engine",
    "APIANT Logo": "APIANT 로고",
    "APIANT MCP Servers provide protocol-level connectivity for AI systems to interact with the APIANT integration platform.":
        "APIANT MCP Servers는 AI 시스템이 APIANT 통합 플랫폼과 상호작용할 수 있는 프로토콜 수준의 연결을 제공합니다.",
    "APIANT Partners": "APIANT 파트너",
    "APIANT Platform Cost": "APIANT 플랫폼 비용",
    "APIANT agents operate inside the full integration platform with access to 500+ connectors, your automations, and your business logic. Goal-driven agents that orchestrate multi-step workflows, query live data across systems, and take action based on real business context.":
        "APIANT agents는 500개 이상의 커넥터, 자동화, 비즈니스 로직에 접근하며 전체 통합 플랫폼 내에서 운영됩니다. 목표 지향적 에이전트가 다단계 워크플로우를 조율하고, 시스템 전체에서 실시간 데이터를 조회하고, 실제 비즈니스 맥락을 기반으로 조치를 취합니다.",
    "APIANT builds your first integrations. You validate the results. Expand when ready.":
        "APIANT가 첫 번째 통합을 구축합니다. 결과를 검증하세요. 준비되면 확장하세요.",
    "APIANT enforces this architecturally. Every automation has a settings layer customizable per deployment without touching logic. One codebase serves 228 Exercise Coach locations, each configured differently, all upgraded simultaneously. Settings surface directly in FormApps for a clean, branded configuration UI.":
        "APIANT는 이를 아키텍처 수준에서 적용합니다. 모든 자동화에는 로직을 건드리지 않고 배포별로 맞춤 설정 가능한 설정 계층이 있습니다. 하나의 코드베이스가 228개 Exercise Coach 지점에 서비스하며, 각각 다르게 구성되고, 모두 동시에 업그레이드됩니다. 설정은 깔끔한 브랜드 구성 UI를 위해 FormApps에 직접 표시됩니다.",
    "APIANT for Enterprises | Bridge the Deep Integration Gap":
        "기업용 APIANT | 깊은 통합 격차 해소",
    "APIANT for SaaS Companies | Own Your Integration Infrastructure":
        "SaaS 회사용 APIANT | 통합 인프라를 소유하세요",
    "APIANT for System Integrators | Turn Expertise Into Recurring Revenue":
        "시스템 통합업체용 APIANT | 전문성을 반복 수익으로 전환",
    "APIANT gives": "APIANT는",
    "APIANT gives SaaS companies and System Integrators a dedicated, white-label integration platform with AI co-pilots, embeddable UIs, and the deepest automation engine on the market.":
        "APIANT는 SaaS 회사와 시스템 통합업체에 AI co-pilot, 임베드 가능한 UI, 시장에서 가장 심층적인 자동화 엔진을 갖춘 전용 화이트 라벨 통합 플랫폼을 제공합니다.",
    "APIANT gives you a dedicated integration platform: your own servers, your own brand, fully managed by us. Assign a workflow architect (not a developer) to build and manage integrations using our visual tools and AI Co-Pilot. Your engineering team stays focused on your product.":
        "APIANT는 전용 통합 플랫폼을 제공합니다. 자체 서버, 자체 브랜드, 완전히 관리됩니다. 워크플로우 아키텍트(개발자가 아닌)를 배정하여 시각적 도구와 AI Co-Pilot을 사용해 통합을 구축하고 관리하세요. 엔지니어링 팀은 제품에 집중할 수 있습니다.",
    "APIANT gives you that platform.": "APIANT가 그 플랫폼을 제공합니다.",
    "APIANT gives your enterprise a dedicated integration server: fully managed infrastructure, your own environment, complete visibility. Build, deploy, and monitor deep integrations across every department without writing code.":
        "APIANT는 기업에 전용 통합 서버를 제공합니다. 완전 관리 인프라, 자체 환경, 완전한 가시성. 코드 작성 없이 모든 부서에 걸쳐 심층 통합을 구축, 배포, 모니터링하세요.",
    "APIANT is the platform of choice for builders": "APIANT는 빌더들이 선택하는 플랫폼입니다",
    "APIANT logs every API call, every data access, and every action taken. Your DPO gets a complete audit trail for every DSAR, automatically.":
        "APIANT는 모든 API 호출, 모든 데이터 접근, 모든 수행 조치를 기록합니다. DPO는 모든 DSAR에 대한 완전한 감사 추적을 자동으로 받습니다.",
    "APIANT manages servers, you manage integrations": "APIANT가 서버를 관리하고, 여러분이 통합을 관리합니다",
    "APIANT manages the infrastructure: servers, uptime, scaling, platform updates":
        "APIANT가 인프라를 관리합니다: 서버, 가동 시간, 확장, 플랫폼 업데이트",
    "APIANT manages the servers, the uptime, the scaling, and the platform updates. You focus on what you're best at: building integrations and serving customers. We handle everything else.":
        "APIANT가 서버, 가동 시간, 확장, 플랫폼 업데이트를 관리합니다. 가장 잘하는 일에 집중하세요: 통합 구축과 고객 서비스. 나머지는 모두 저희가 처리합니다.",
    "APIANT queries HubSpot, Zendesk, Stripe, your email system, and analytics database simultaneously":
        "APIANT가 HubSpot, Zendesk, Stripe, 이메일 시스템, 분석 데이터베이스를 동시에 조회합니다",
    "APIANT started as a system integrator. We built integration products for clients, realized we needed a better platform, and built our own. Today we run 17 integration products on the same platform we're offering you, serving thousands of businesses with sub-1% churn. We didn't build a platform and go looking for users. We were the users first.":
        "APIANT는 시스템 통합업체로 시작했습니다. 고객을 위해 통합 제품을 구축하다가 더 나은 플랫폼이 필요하다는 것을 깨닫고 직접 만들었습니다. 오늘날 여러분에게 제공하는 것과 동일한 플랫폼에서 17개 통합 제품을 운영하며, 1% 미만의 이탈률로 수천 개의 비즈니스에 서비스하고 있습니다. 플랫폼을 만들고 사용자를 찾은 것이 아닙니다. 우리가 먼저 사용자였습니다.",
    "APIANT started as an SI. We built integration products for clients, realized we needed a better platform, and built our own.":
        "APIANT는 SI로 시작했습니다. 고객을 위해 통합 제품을 구축하다가 더 나은 플랫폼이 필요하다는 것을 깨닫고 직접 만들었습니다.",
    "APIANT supports teams of all sizes, with pricing that scales.":
        "APIANT는 모든 규모의 팀을 지원하며, 확장 가능한 가격을 제공합니다.",
    "APIANT | 250+ Apps, Thousands of Connectors": "APIANT | 250개 이상의 앱, 수천 개의 커넥터",
    "APIANT | The Integration Platform Builders Own": "APIANT | 빌더가 소유하는 통합 플랫폼",
    "APIANT's AI is platform-native, not bolted-on. From an AI Co-Pilot that builds connectors to autonomous agents with access to 500+ integrations, this is AI that operates inside the full integration platform.":
        "APIANT의 AI는 플랫폼 네이티브이며, 단순 부착이 아닙니다. 커넥터를 구축하는 AI Co-Pilot부터 500개 이상의 통합에 접근하는 자율 에이전트까지, 전체 통합 플랫폼 내에서 운영되는 AI입니다.",
    "APIANT's AI operates inside the full integration platform. Assembly Editor AI Co-Pilot, AI Agents with goals and tools, and an AI Chatbot with infinite possibilities.":
        "APIANT의 AI는 전체 통합 플랫폼 내에서 운영됩니다. Assembly Editor AI Co-Pilot, 목표와 도구를 가진 AI Agents, 무한한 가능성의 AI Chatbot.",
    "APIANT's MCP servers expose your automations and connectors as tools that AI models can call natively. This is not a wrapper or an adapter - it is protocol-level interoperability between AI and your integration layer.":
        "APIANT의 MCP servers는 자동화와 커넥터를 AI 모델이 네이티브로 호출할 수 있는 도구로 노출합니다. 래퍼나 어댑터가 아닙니다. AI와 통합 레이어 간의 프로토콜 수준 상호 운용성입니다.",
    "APIANT's unified data processing engine normalizes every format into a single internal model before transformation. The result: linear scaling regardless of format, massive payloads handled natively (no batch splitting, no hard limits), and one consistent way to query and transform data across any API. This is the foundation the entire platform is built on.":
        "APIANT의 통합 데이터 처리 엔진은 변환 전에 모든 형식을 단일 내부 모델로 정규화합니다. 결과: 형식에 관계없이 선형 확장, 대규모 페이로드의 네이티브 처리(배치 분할 없음, 하드 리밋 없음), 모든 API에서 데이터를 조회하고 변환하는 하나의 일관된 방법. 이것이 전체 플랫폼이 구축된 기반입니다.",
    "Absolutely. ZoomConnect can send instructors a secure \"Start Class\" link via email, eliminating the need to share Zoom account credentials and simplifying the process for instructors to begin their sessions.":
        "물론입니다. ZoomConnect는 강사에게 이메일로 안전한 \"수업 시작\" 링크를 보내, Zoom 계정 자격 증명을 공유할 필요 없이 강사가 간편하게 세션을 시작할 수 있도록 합니다.",
    "Accept credit cards instantly with Shopify Payments - no third-party accounts needed - or choose from over 100 global payment gateways for secure, seamless transactions worldwide.":
        "Shopify Payments로 신용카드를 즉시 결제하세요. 타사 계정이 필요 없습니다. 또는 전 세계 100개 이상의 결제 게이트웨이에서 선택하여 안전하고 원활한 거래를 진행하세요.",
    "Access Control": "접근 제어",
    "Access comprehensive client insights, enabling precise segmentation, targeted communication, and more effective client engagement.":
        "포괄적인 고객 인사이트에 접근하여 정밀한 세분화, 타겟 커뮤니케이션, 더 효과적인 고객 참여를 가능하게 합니다.",
    "Access critical details to automate timely reminders, personalized messaging, and targeted follow-ups - ensuring every client receives the right communication exactly when it matters most.":
        "적시 리마인더, 개인화 메시지, 타겟 후속 조치를 자동화하는 핵심 세부 정보에 접근하여, 모든 고객이 가장 중요한 순간에 적절한 커뮤니케이션을 받도록 합니다.",
    "Access to 500+ Connectors": "500개 이상의 커넥터 접근",
    "Account Network": "계정 네트워크",
    "Account Networks": "계정 네트워크",
    "Account connection": "계정 연결",
    "Account networks let a master account manage hundreds of child accounts, each representing a location or customer. New locations inherit shared connections and settings automatically. Set rate limits at the platform level - the system enforces them across all accounts. Deploy codebase upgrades to every linked account simultaneously with one click.":
        "계정 네트워크를 통해 마스터 계정이 수백 개의 하위 계정을 관리할 수 있으며, 각각 지점이나 고객을 나타냅니다. 신규 지점은 공유 연결과 설정을 자동으로 상속받습니다. 플랫폼 수준에서 속도 제한을 설정하면 시스템이 모든 계정에 적용합니다. 한 번의 클릭으로 모든 연결된 계정에 코드베이스 업그레이드를 동시에 배포합니다.",
    "Account-Level Permissions": "계정 수준 권한",
    "Accurate Taxes & Discounts": "정확한 세금 및 할인",
    "Accurate Taxes and Discounts": "정확한 세금 및 할인",
    "Accurately capture and sync essential client details from Calendly to Mindbody, ensuring up-to-date client records and improved engagement.":
        "Calendly에서 Mindbody로 필수 고객 세부 정보를 정확하게 캡처하고 동기화하여, 최신 고객 기록과 향상된 참여를 보장합니다.",
    "Accurately capture and sync essential client details from Calendly to Mindbody. New clients are automatically created, and existing records stay up-to-date with every booking.":
        "Calendly에서 Mindbody로 필수 고객 세부 정보를 정확하게 캡처하고 동기화합니다. 신규 고객은 자동으로 생성되며, 기존 기록은 모든 예약과 함께 최신 상태를 유지합니다.",
    "Acme Inc.": "Acme Inc.",
    "Action": "액션",
    "Actions": "액션",
    "Actions, triggers, or both. It knows which APIs are read-only and which support writes. Generates input fields, settings, and UI controls for each operation.":
        "액션, 트리거, 또는 둘 다. 어떤 API가 읽기 전용이고 어떤 API가 쓰기를 지원하는지 파악합니다. 각 작업에 대한 입력 필드, 설정, UI 컨트롤을 생성합니다.",
    "Active": "활성",
    "ActiveCampaign Partner": "ActiveCampaign 파트너",
    "ActiveCampaign clearly tracks donor activity, campaign effectiveness, and fundraising performance, giving you easy-to-understand insights to guide your fundraising strategy.":
        "ActiveCampaign은 기부자 활동, 캠페인 효과, 모금 성과를 명확하게 추적하여, 모금 전략을 안내할 이해하기 쉬운 인사이트를 제공합니다.",
    "ActiveCampaign helps you clearly connect customer actions - like purchases or membership sign-ups - to specific marketing activities. Easily measure how well your campaigns and channels perform, so you can see exactly what's driving your ROI.":
        "ActiveCampaign은 구매나 멤버십 가입과 같은 고객 행동을 특정 마케팅 활동에 명확하게 연결하는 데 도움을 줍니다. 캠페인과 채널의 성과를 쉽게 측정하여, ROI를 이끄는 요소를 정확히 파악할 수 있습니다.",
    "Activity Tracking": "활동 추적",
    "Additional Connections": "추가 연결",
    "Additional DonorPerfect filters:": "추가 DonorPerfect 필터:",
    "Additional Mindbody Locations:": "추가 Mindbody 지점:",
    "Additional Mindbody appointment types:": "추가 Mindbody 예약 유형:",
    "Additional Mindbody locations:": "추가 Mindbody 지점:",
    "Additional Zoom accounts connected:": "추가 연결된 Zoom 계정:",
    "Additional payloads:": "추가 payload:",
    "Admin Console": "Admin Console",
    "Admin Console [Main]: Automations": "Admin Console [메인]: 자동화",
    "Admin Console showing account network with linked accounts": "연결된 계정과 계정 네트워크를 보여주는 Admin Console",
    "Admin Console | APIANT": "Admin Console | APIANT",
    "Admin Console | Your Control Center": "Admin Console | 제어 센터",
    "Advanced Fundraising Tools": "고급 모금 도구",
    "Advanced logic for handling complex scenarios like bulk bookings, cancellations, and schedule changes":
        "대량 예약, 취소, 일정 변경과 같은 복잡한 시나리오를 처리하기 위한 고급 로직",
    "Advanced logic for handling complex scenarios like bulk donations, recurring gifts, and campaign tracking":
        "대량 기부, 정기 기부, 캠페인 추적과 같은 복잡한 시나리오를 처리하기 위한 고급 로직",
    "Advertising ROI Reporting": "광고 ROI 보고",
    "Advertising ROI Reports": "광고 ROI 보고서",
    "Advertising ROI Tracking": "광고 ROI 추적",
    "Advertising ROI reports require HubSpot Marketing Hub Enterprise. You can connect your ad accounts and configure reports directly in HubSpot.":
        "광고 ROI 보고서에는 HubSpot Marketing Hub Enterprise가 필요합니다. HubSpot에서 직접 광고 계정을 연결하고 보고서를 구성할 수 있습니다.",
    "Affordable Per-Booking Pricing": "합리적인 건당 예약 가격",
    "Affordable Pricing": "합리적인 가격",
    "Affordable and flexible pricing to scale with your business": "비즈니스와 함께 확장되는 합리적이고 유연한 가격",
    "Agents don't operate in a vacuum. They have access to every connector on the APIANT platform (CRMs, ERPs, marketing tools, databases, custom APIs) all of them.":
        "에이전트는 진공 상태에서 작동하지 않습니다. APIANT 플랫폼의 모든 커넥터(CRM, ERP, 마케팅 도구, 데이터베이스, 맞춤 API)에 접근할 수 있습니다.",
    "Agents that autonomously interact with CRMs, ERPs, scheduling platforms, and more through APIANT's connector library.":
        "APIANT의 커넥터 라이브러리를 통해 CRM, ERP, 일정 관리 플랫폼 등과 자율적으로 상호작용하는 에이전트.",
    "Agents with Goals, Tools, and the Whole Platform Behind Them":
        "목표, 도구, 그리고 전체 플랫폼이 뒷받침하는 에이전트",
    "Agents with goals, tools, and the whole platform behind them. While others bolt AI onto standalone chatbots, APIANT agents operate inside the full integration platform, with access to 500+ connectors, your automations, and your business logic.":
        "목표, 도구, 그리고 전체 플랫폼이 뒷받침하는 에이전트. 다른 곳에서 독립 챗봇에 AI를 부착하는 반면, APIANT 에이전트는 500개 이상의 커넥터, 자동화, 비즈니스 로직에 접근하며 전체 통합 플랫폼 내에서 운영됩니다.",
    "Alec Whitten • 17 Jan 2022": "Alec Whitten • 2022년 1월 17일",
    "All CRMConnect users connecting DonorPerfect and Keap are nonprofits; thus, our pricing is already optimized for nonprofits.":
        "DonorPerfect와 Keap을 연결하는 모든 CRMConnect 사용자는 비영리 단체이므로, 가격은 이미 비영리 단체에 최적화되어 있습니다.",
    "All Categories": "모든 카테고리",
    "All Pro features, plus:": "모든 Pro 기능 포함, 추가:",
    "All Rights Reserved.": "모든 권리 보유.",
    "All Sandbox features, plus:": "모든 Sandbox 기능 포함, 추가:",
    "All standard donor and donation fields sync automatically; specific custom fields require optional customization.":
        "모든 표준 기부자 및 기부 필드가 자동으로 동기화됩니다. 특정 맞춤 필드에는 선택적 맞춤 설정이 필요합니다.",
    "Allow customers to choose delivery or convenient in-person pickup from any connected location, with seamless order routing automatically handled for you.":
        "고객이 배송 또는 연결된 모든 지점에서 편리한 현장 수령을 선택할 수 있도록 하며, 원활한 주문 라우팅이 자동으로 처리됩니다.",
    "Allow instructors to simultaneously teach Zoom classes to clients booked from multiple linked Mindbody Site IDs, across different time zones - unlocking powerful opportunities for virtual fitness.":
        "강사가 여러 Mindbody Site ID에서 예약된 고객에게 다양한 시간대에 걸쳐 Zoom 수업을 동시에 진행할 수 있도록 하여, 가상 피트니스의 강력한 기회를 열어줍니다.",
    "Allow instructors to simultaneously teach Zoom classes to clients booked from multiple linked Mindbody Site IDs, across different time zones.":
        "강사가 여러 Mindbody Site ID에서 예약된 고객에게 다양한 시간대에 걸쳐 Zoom 수업을 동시에 진행할 수 있도록 합니다.",
    "Already using one of these platforms? We have a turnkey product ready for you.":
        "이미 이러한 플랫폼을 사용하고 계신가요? 즉시 사용 가능한 턴키 제품이 준비되어 있습니다.",
    "Always Up-to-Date Donor Segments": "항상 최신 상태의 기부자 세그먼트",
    "Always know each client's most recent visit details - date, type, staff member, and service - to trigger timely follow-ups and engagement campaigns.":
        "각 고객의 최근 방문 세부 정보(날짜, 유형, 담당 직원, 서비스)를 항상 파악하여 적시 후속 조치와 참여 캠페인을 트리거합니다.",
    "Always know when patients are scheduled or overdue for their next visit. Appointment details sync automatically into HubSpot, enabling reminders, no-show recovery, and gentle recall nudges for inactive patients.":
        "환자의 다음 방문 예정일과 연체 여부를 항상 파악합니다. 예약 세부 정보가 HubSpot에 자동으로 동기화되어, 리마인더, 노쇼 복구, 비활성 환자에 대한 부드러운 리콜 알림을 가능하게 합니다.",
    "An AI agent monitoring your CRM can detect when a high-value client's engagement pattern changes, cross-reference their recent support tickets, check their upcoming renewal date, and proactively alert the account team with a recommended action plan, all without anyone asking it to.":
        "CRM을 모니터링하는 AI 에이전트가 고가치 고객의 참여 패턴 변화를 감지하고, 최근 지원 티켓을 교차 참조하고, 다가오는 갱신일을 확인하고, 추천 실행 계획과 함께 계정팀에 사전 알림을 보낼 수 있습니다. 누군가 요청하지 않아도 자동으로 수행됩니다.",
    "An APIANT AI Chatbot is deceptively simple in structure: a trigger (the user's message) and an action (the response). But between those two points lies the full power of the platform: AI, conditionals, data lookups, other automations, and any logic you can design.":
        "APIANT AI Chatbot은 구조적으로 놀라울 정도로 단순합니다. 트리거(사용자 메시지)와 액션(응답). 하지만 이 두 지점 사이에 플랫폼의 모든 기능이 있습니다: AI, 조건문, 데이터 조회, 다른 자동화, 설계 가능한 모든 로직.",
    "An APIANT chatbot is deceptively simple: a trigger (the user's message) and an action (the response). But between those two points lies the full power of the platform: AI reasoning, API calls to any connected system, data transformation, conditional logic, and multi-step workflows.":
        "APIANT 챗봇은 놀라울 정도로 단순합니다. 트리거(사용자 메시지)와 액션(응답). 하지만 이 두 지점 사이에 플랫폼의 모든 기능이 있습니다: AI 추론, 연결된 모든 시스템에 대한 API 호출, 데이터 변환, 조건부 로직, 다단계 워크플로우.",
    "Analytics database": "분석 데이터베이스",
    "Angie P.": "Angie P.",
    "Animated diagram showing JSON, XML, CSV, and SOAP data flowing into the APIANT Unified XML Engine and emerging as normalized data":
        "JSON, XML, CSV, SOAP 데이터가 APIANT 통합 XML 엔진으로 유입되어 정규화된 데이터로 변환되는 애니메이션 다이어그램",
    "Annotation": "주석",
    "Annual Profit": "연간 수익",
    "Any Format, Same Performance": "모든 형식, 동일한 성능",
    "Any app. Stripe, Asana, a niche veterinary management system. If it has an API, the Co-Pilot can work with it.":
        "모든 앱. Stripe, Asana, 니치 동물병원 관리 시스템. API가 있다면 Co-Pilot이 작업할 수 있습니다.",
    "Any paid ActiveCampaign subscription works with CRMConnect.":
        "모든 유료 ActiveCampaign 구독이 CRMConnect와 호환됩니다.",
    "Anyone, which is the problem": "누구나, 그것이 문제입니다",
    "App Catalog": "앱 카탈로그",
    "AppConnect bridges Mindbody and Zapier, connecting Mindbody to thousands of apps to automate workflows and eliminate busywork--no coding required.":
        "AppConnect는 Mindbody와 Zapier를 연결하여, Mindbody를 수천 개의 앱에 연결하고 워크플로우를 자동화하며 반복 작업을 제거합니다. 코딩이 필요 없습니다.",
    "AppConnect Mindbody and Zapier": "AppConnect Mindbody 및 Zapier",
    "AppConnect goes far beyond Zapier's native Mindbody connector. Every event triggers instantly via webhooks and is enriched with additional API calls, delivering detailed, comprehensive data to power your automations.":
        "AppConnect는 Zapier의 기본 Mindbody 커넥터를 훨씬 뛰어넘습니다. 모든 이벤트가 webhook을 통해 즉시 트리거되고 추가 API 호출로 보강되어, 자동화를 구동하는 상세하고 포괄적인 데이터를 제공합니다.",
    "AppConnect is an easy-to-use integration tool that seamlessly connects your Mindbody account with thousands of popular apps through Zapier - automating workflows, eliminating manual tasks, and boosting productivity without any coding.":
        "AppConnect는 Mindbody 계정을 Zapier를 통해 수천 개의 인기 앱과 원활하게 연결하는 사용하기 쉬운 통합 도구입니다. 워크플로우를 자동화하고, 수동 작업을 제거하고, 코딩 없이 생산성을 높입니다.",
    "Appointment Booking Management": "예약 관리",
    "Appointment Booking Sync": "예약 동기화",
    "Appointment Completion Tagging": "예약 완료 태그 지정",
    "Appointment Deal Amount": "예약 거래 금액",
    "Appointment Pack Tracking": "예약 패키지 추적",
    "Appointment Sync": "예약 동기화",
    "Appointment Sync & Tracking": "예약 동기화 및 추적",
    "Appointment Sync and Tracking": "예약 동기화 및 추적",
    "Appointment Sync to Salesforce": "Salesforce로 예약 동기화",
    "Appointment Tracking": "예약 추적",
    "Appointment pipeline": "예약 파이프라인",
    "Appointment sync": "예약 동기화",
    "Appointment tagging": "예약 태그 지정",
    "Appointments > HL Calendar": "예약 > HL 캘린더",
    "Appointments Pipeline": "예약 파이프라인",
    "Appointments Sync & Pipeline": "예약 동기화 및 파이프라인",
    "Appointments Sync & Pipeline:": "예약 동기화 및 파이프라인:",
    "Appointments and classes sync 7 days back and 30 days forward by default; sales data syncs from the previous month.":
        "예약과 수업은 기본적으로 과거 7일, 미래 30일까지 동기화되며, 판매 데이터는 전월부터 동기화됩니다.",
    "Appointments, Client Services, Memberships, Contracts, Purchases, Purchased Items, and Payments each sync into dedicated custom objects within Zoho CRM.":
        "예약, 고객 서비스, 멤버십, 계약, 구매, 구매 항목, 결제가 각각 Zoho CRM 내의 전용 맞춤 오브젝트로 동기화됩니다.",
    "Appointments, class bookings and attendance, visits, and sales line items automatically sync into Klaviyo profiles.":
        "예약, 수업 예약 및 출석, 방문, 판매 항목이 자동으로 Klaviyo 프로필에 동기화됩니다.",
    "Apps, Thousands of Connectors": "앱, 수천 개의 커넥터",
    "Architectural Advantage": "아키텍처 우위",
    "Architecture": "아키텍처",
    "Are ActiveCampaign automations and campaign building included?": "ActiveCampaign 자동화 및 캠페인 구축이 포함되나요?",
    "Are ActiveCampaign automations included?": "ActiveCampaign 자동화가 포함되나요?",
    "Are HubSpot workflows and sequences included?": "HubSpot 워크플로우와 시퀀스가 포함되나요?",
    "Are Klaviyo automations included?": "Klaviyo 자동화가 포함되나요?",
    "Are Zoho CRM workflows and automations included?": "Zoho CRM 워크플로우와 자동화가 포함되나요?",
    "Are appointments, cases, invoices and payments two-way synced?": "예약, 케이스, 인보이스, 결제가 양방향 동기화되나요?",
    "Are automations in Keap included?": "Keap의 자동화가 포함되나요?",
    "Are automations included?": "자동화가 포함되나요?",
    "Are bookings, visits, sales, memberships, and contracts two-way?": "예약, 방문, 판매, 멤버십, 계약이 양방향인가요?",
    "Are class bookings and attendance, visits, sales, appointments, membership, and contracts two-way synced?":
        "수업 예약 및 출석, 방문, 판매, 예약, 멤버십, 계약이 양방향 동기화되나요?",
    "Are there extra costs for syncing large numbers of donations?": "대량의 기부금을 동기화하면 추가 비용이 발생하나요?",
    "Ask the Co-Pilot to build an endpoint...": "Co-Pilot에게 엔드포인트 구축을 요청하세요...",
    "Ask the chatbot \"What's the revenue this month?\" or \"How many orders are pending?\" and it queries your ERP, accounting system, and warehouse management in real time.":
        "챗봇에게 \"이번 달 매출은?\" 또는 \"보류 중인 주문은 몇 건?\"이라고 물으면 ERP, 회계 시스템, 창고 관리 시스템을 실시간으로 조회합니다.",
    "Ask the chatbot to pull reports, update records, sync data across systems, or trigger workflows, via natural language.":
        "챗봇에게 자연어로 보고서 추출, 기록 업데이트, 시스템 간 데이터 동기화, 워크플로우 트리거를 요청하세요.",
    "Assemblies create": "Assembly 생성",
    "Assemblies create the building blocks. Automations wire them together. The Admin Console deploys them at scale.":
        "Assembly가 빌딩 블록을 생성합니다. 자동화가 이를 연결합니다. Admin Console이 대규모로 배포합니다.",
    "Assembly Editor": "Assembly Editor",
    "Assembly Editor + AI Co-Pilot": "Assembly Editor + AI Co-Pilot",
    "Assembly Editor + AI Co-Pilot | APIANT": "Assembly Editor + AI Co-Pilot | APIANT",
    "Assembly Editor + AI Co-Pilot | The AI That Reads API Docs So You Don't Have To":
        "Assembly Editor + AI Co-Pilot | API 문서를 대신 읽어주는 AI",
    "Assembly Editor AI Co-Pilot": "Assembly Editor AI Co-Pilot",
    "Assembly diagram version:": "Assembly 다이어그램 버전:",
    "Assign roles to team members -- administrators, builders, viewers. Each role defines what actions a user can take and which accounts they can access within the network.":
        "팀 구성원에게 역할을 할당합니다. 관리자, 빌더, 뷰어. 각 역할은 사용자가 수행할 수 있는 작업과 네트워크 내에서 접근할 수 있는 계정을 정의합니다.",
    "Attendance tracking": "출석 추적",
    "Audit trail coverage for compliance reporting": "컴플라이언스 보고를 위한 감사 추적 범위",
    "Authentication setup": "인증 설정",
    "Authentication:": "인증:",
    "Auto-completion, intelligent defaults, and AI-driven validation powered by the platform's native AI capabilities.":
        "플랫폼의 네이티브 AI 기능으로 구동되는 자동 완성, 지능형 기본값, AI 기반 검증.",
    "Automate": "자동화",
    "Automated Custom Fields": "자동화된 맞춤 필드",
    "Automated Custom Fields Creation": "자동화된 맞춤 필드 생성",
    "Automated Emails & SMS": "자동화된 이메일 및 SMS",
    "Automated Emails and SMS": "자동화된 이메일 및 SMS",
    "Automated Follow-Ups & Thank-Yous": "자동화된 후속 조치 및 감사 메시지",
    "Automated Follow-Ups and Thank-Yous": "자동화된 후속 조치 및 감사 메시지",
    "Automated, bidirectional updates that maintain data accuracy across all connected systems":
        "모든 연결된 시스템에서 데이터 정확성을 유지하는 자동화된 양방향 업데이트",
    "Automatic": "자동",
    "Automatic Appointment Sync": "자동 예약 동기화",
    "Automatic Client Creation": "자동 고객 생성",
    "Automatic Custom Fields": "자동 맞춤 필드",
    "Automatic Data Management": "자동 데이터 관리",
    "Automatic Data Updates": "자동 데이터 업데이트",
    "Automatic Donor Data Sync": "자동 기부자 데이터 동기화",
    "Automatic Donor Sync": "자동 기부자 동기화",
    "Automatic Dropdown \"CodeSync\"": "자동 드롭다운 \"CodeSync\"",
    "Automatic Dropdown CodeSync": "자동 드롭다운 CodeSync",
    "Automatic Lead Routing": "자동 리드 라우팅",
    "Automatic Roll Call": "자동 출석 확인",
    "Automatic Shopify-to-Mindbody Sales": "Shopify에서 Mindbody로 자동 판매",
    "Automatic Zoom Meeting Creation": "자동 Zoom 미팅 생성",
    "Automatic Zoom Meetings": "자동 Zoom 미팅",
    "Automatic Zoom link creation": "자동 Zoom 링크 생성",
    "Automatic donor sync": "자동 기부자 동기화",
    "Automatically add or update client profiles in Mindbody from lead sources like Meta ad campaigns, and seamlessly enroll clients into classes - streamlining your marketing, sales, and onboarding workflows.":
        "Meta 광고 캠페인과 같은 리드 소스에서 Mindbody의 고객 프로필을 자동으로 추가하거나 업데이트하고, 고객을 수업에 원활하게 등록하여 마케팅, 영업, 온보딩 워크플로우를 간소화합니다.",
    "Automatically apply tags to ActiveCampaign contacts when they complete appointments in Cliniko. Create targeted segments and deliver timely, relevant communications that improve patient engagement.":
        "Cliniko에서 예약을 완료하면 ActiveCampaign 연락처에 자동으로 태그를 적용합니다. 타겟 세그먼트를 생성하고 환자 참여를 향상시키는 적시의 관련 커뮤니케이션을 제공합니다.",
    "Automatically assign a value to each appointment deal based on billable items. Get clear insight into the financial value of every session, helping you forecast revenue and make smarter business decisions.":
        "청구 가능 항목을 기반으로 각 예약 거래에 자동으로 값을 할당합니다. 모든 세션의 재무 가치에 대한 명확한 인사이트를 얻어, 매출을 예측하고 더 현명한 비즈니스 의사결정을 할 수 있습니다.",
    "Automatically capture every client purchase from Mindbody - including dates, intro offers, services, and products - directly in HubSpot. Leverage detailed purchase histories and itemized data to power personalized communications, drive conversions, enhance retention, and boost your revenue.":
        "날짜, 체험 상품, 서비스, 제품을 포함한 Mindbody의 모든 고객 구매를 HubSpot에 직접 자동으로 캡처합니다. 상세한 구매 이력과 항목별 데이터를 활용하여 개인화 커뮤니케이션을 구동하고, 전환을 촉진하고, 유지율을 높이고, 매출을 증가시킵니다.",
    "Automatically capture every client purchase, individual items bought, and payment statuses. Leverage this detailed data for precise sales tracking, targeted marketing, and crystal-clear financial visibility.":
        "모든 고객 구매, 개별 구매 항목, 결제 상태를 자동으로 캡처합니다. 이 상세 데이터를 활용하여 정밀한 판매 추적, 타겟 마케팅, 명확한 재무 가시성을 확보합니다.",
    "Automatically capture every client purchase, individual items bought, and payment statuses. Leverage this detailed data for precise sales tracking, targeted marketing, granular client segmentation, and crystal-clear financial visibility.":
        "모든 고객 구매, 개별 구매 항목, 결제 상태를 자동으로 캡처합니다. 이 상세 데이터를 활용하여 정밀한 판매 추적, 타겟 마케팅, 세분화된 고객 세그멘테이션, 명확한 재무 가시성을 확보합니다.",
    "Automatically capture recent client visits, providing opportunities for post-visit follow-ups and re-engagement sequences.":
        "최근 고객 방문을 자동으로 캡처하여, 방문 후 후속 조치 및 재참여 시퀀스 기회를 제공합니다.",
    "Automatically convert DonorPerfect flags into Keap tags, streamlining segmentation for effective targeting and personalized donor journeys.":
        "DonorPerfect 플래그를 Keap 태그로 자동 변환하여, 효과적인 타겟팅과 개인화된 기부자 여정을 위한 세그멘테이션을 간소화합니다.",
    "Automatically create Mindbody appointments directly from Calendly bookings, instantly reflecting changes and new bookings.":
        "Calendly 예약에서 Mindbody 예약을 직접 자동 생성하여, 변경 사항과 새 예약을 즉시 반영합니다.",
    "Automatically create Mindbody appointments directly from Calendly bookings. Every new booking, reschedule, and cancellation is instantly reflected - no manual entry required.":
        "Calendly 예약에서 Mindbody 예약을 직접 자동 생성합니다. 모든 새 예약, 일정 변경, 취소가 즉시 반영되며, 수동 입력이 필요 없습니다.",
    "Automatically create a live appointment pipeline in ActiveCampaign, clearly tracking booking statuses, schedule changes, and remaining sessions.":
        "ActiveCampaign에서 실시간 예약 파이프라인을 자동 생성하여, 예약 상태, 일정 변경, 잔여 세션을 명확하게 추적합니다.",
    "Automatically generate thank-you emails, receipts, and personalized follow-up communications based on updated donor actions and history.":
        "업데이트된 기부자 활동과 이력을 기반으로 감사 이메일, 영수증, 개인화된 후속 커뮤니케이션을 자동 생성합니다.",
    "Automatically itemize each client purchase within HubSpot's Mindbody Sales Pipeline. Clearly connect revenue to specific marketing campaigns, coaching efforts, staff activities, and more - enabling precise measurement and actionable insights for continuous improvement.":
        "HubSpot의 Mindbody Sales Pipeline에서 각 고객 구매를 자동으로 항목화합니다. 매출을 특정 마케팅 캠페인, 코칭 노력, 직원 활동 등에 명확하게 연결하여, 지속적인 개선을 위한 정밀한 측정과 실행 가능한 인사이트를 제공합니다.",
    "Automatically keep Cliniko patient profiles and HubSpot contacts perfectly synced in real-time. Demographics, preferences, appointment history, and 120+ key properties flow between platforms so your team always works with accurate data.":
        "Cliniko 환자 프로필과 HubSpot 연락처를 실시간으로 완벽하게 동기화합니다. 인구통계, 선호도, 예약 이력, 120개 이상의 핵심 속성이 플랫폼 간에 흐르므로 팀은 항상 정확한 데이터로 작업합니다.",
    "Automatically keep Mindbody client profiles and ActiveCampaign contacts in perfect step, and push any tagged lead from ActiveCampaign straight into the right Mindbody site.":
        "Mindbody 고객 프로필과 ActiveCampaign 연락처를 완벽하게 동기화하고, ActiveCampaign에서 태그된 리드를 올바른 Mindbody 사이트로 직접 전달합니다.",
    "Automatically keep Mindbody client profiles and HubSpot contacts fully synchronized. Easily push selected HubSpot contacts into any connected Mindbody location - manually or via automated workflows - ensuring accurate, consistent client data across all your systems":
        "Mindbody 고객 프로필과 HubSpot 연락처를 완전히 동기화합니다. 선택한 HubSpot 연락처를 수동 또는 자동화 워크플로우를 통해 연결된 모든 Mindbody 지점으로 쉽게 전달하여, 모든 시스템에서 정확하고 일관된 고객 데이터를 보장합니다.",
    "Automatically keep Mindbody client profiles and Keap contacts perfectly synced in real-time. Changes in either platform flow instantly to the other, so your team always works with accurate data.":
        "Mindbody 고객 프로필과 Keap 연락처를 실시간으로 완벽하게 동기화합니다. 어느 플랫폼에서든 변경 사항이 즉시 다른 플랫폼으로 전달되므로, 팀은 항상 정확한 데이터로 작업합니다.",
    "Automatically keep your Mindbody products (including pricing, taxes, descriptions, images, sizes, colors, inventory, and variants) consistently updated in Shopify, simply by marking items as \"Sell Online.\"":
        "항목을 \"온라인 판매\"로 표시하기만 하면, Mindbody 제품(가격, 세금, 설명, 이미지, 사이즈, 색상, 재고, 변형 포함)이 Shopify에서 일관되게 업데이트됩니다.",
    "Automatically keep your Mindbody products - including pricing, taxes, descriptions, images, sizes, colors, inventory, and variants - consistently updated in Shopify, simply by marking items as \"Sell Online.\"":
        "항목을 \"온라인 판매\"로 표시하기만 하면, Mindbody 제품(가격, 세금, 설명, 이미지, 사이즈, 색상, 재고, 변형 포함)이 Shopify에서 일관되게 업데이트됩니다.",
    "Automatically log every client purchase as a detailed deal, clearly connecting revenue with marketing efforts, staff activities, and follow-ups.":
        "모든 고객 구매를 상세 거래로 자동 기록하여, 매출을 마케팅 노력, 직원 활동, 후속 조치에 명확하게 연결합니다.",
    "Automatically maintain synchronized client profiles between Mindbody and Zoho CRM, effortlessly updating and pushing leads and clients between both systems.":
        "Mindbody와 Zoho CRM 간에 동기화된 고객 프로필을 자동으로 유지하며, 두 시스템 간에 리드와 고객을 손쉽게 업데이트하고 전달합니다.",
    "Automatically maintain synchronized client profiles between Mindbody and Zoho CRM. Updates flow in both directions, so your team always works with accurate, up-to-date data.":
        "Mindbody와 Zoho CRM 간에 동기화된 고객 프로필을 자동으로 유지합니다. 업데이트가 양방향으로 흐르므로, 팀은 항상 정확한 최신 데이터로 작업합니다.",
    "Automatically manage Keap tags based on client purchases, enabling precise segmentation for upsell campaigns, renewal reminders, and personalized communication.":
        "고객 구매를 기반으로 Keap 태그를 자동 관리하여, 업셀 캠페인, 갱신 리마인더, 개인화 커뮤니케이션을 위한 정밀한 세그멘테이션을 가능하게 합니다.",
    "Automatically manage Mailchimp \"cleaned\" email addresses in DonorPerfect, ensuring your data remains reliable and your sender reputation stays strong.":
        "DonorPerfect에서 Mailchimp \"정리된\" 이메일 주소를 자동 관리하여, 데이터의 신뢰성과 발신자 평판을 유지합니다.",
    "Automatically match taxes and discounts applied in Mindbody and Shopify sales, ensuring consistent accuracy across both platforms.":
        "Mindbody와 Shopify 판매에 적용된 세금과 할인을 자동으로 맞추어, 두 플랫폼에서 일관된 정확성을 보장합니다.",
    "Automatically populate ActiveCampaign with over 120 custom fields designed specifically for wellness businesses, enabling deeper segmentation and personalized automations.":
        "웰니스 비즈니스를 위해 특별히 설계된 120개 이상의 맞춤 필드로 ActiveCampaign을 자동으로 채워, 더 깊은 세그멘테이션과 개인화 자동화를 가능하게 합니다.",
    "Automatically populate HubSpot dropdown menus with your DonorPerfect codes (e.g., donor types, campaign types), removing manual entry and ensuring accuracy.":
        "DonorPerfect 코드(예: 기부자 유형, 캠페인 유형)로 HubSpot 드롭다운 메뉴를 자동으로 채워, 수동 입력을 제거하고 정확성을 보장합니다.",
    "Automatically push sales, line items, payment details, and membership status changes from Mindbody to any Zapier-connected app - perfect for financial tracking, retention campaigns, and reporting.":
        "판매, 항목, 결제 세부 정보, 멤버십 상태 변경을 Mindbody에서 Zapier 연결 앱으로 자동 전달합니다. 재무 추적, 유지 캠페인, 보고에 적합합니다.",
    "Automatically reflect your clients' Mindbody activities - including bookings, visits, missed classes, and purchases - in HubSpot. Keep your team informed, enhance client engagement, and deliver timely, personalized communications.":
        "예약, 방문, 결석, 구매를 포함한 고객의 Mindbody 활동을 HubSpot에 자동으로 반영합니다. 팀에 정보를 제공하고, 고객 참여를 향상시키고, 적시의 개인화 커뮤니케이션을 전달합니다.",
    "Automatically refresh donor records in Keap whenever donations are made or updated, including contact information, donation dates, contribution amounts, year-to-date totals, giving history, and key donor metrics.":
        "기부가 이루어지거나 업데이트될 때마다 연락처 정보, 기부 날짜, 기부 금액, 연간 누계, 기부 이력, 주요 기부자 지표를 포함하여 Keap의 기부자 기록을 자동으로 갱신합니다.",
    "Automatically send Zoom links and recordings to clients and staff via email and SMS - simply choose your timing once, and it's seamlessly handled for every class.":
        "이메일과 SMS를 통해 고객과 직원에게 Zoom 링크와 녹화 영상을 자동 전송합니다. 타이밍을 한 번만 설정하면 모든 수업에 원활하게 적용됩니다.",
    "Automatically send Zoom links and recordings to clients and staff via email and SMS. Choose your timing once, and it runs seamlessly for every class.":
        "이메일과 SMS를 통해 고객과 직원에게 Zoom 링크와 녹화 영상을 자동 전송합니다. 타이밍을 한 번만 설정하면 모든 수업에 원활하게 적용됩니다.",
    "Automatically send Zoom links via email or SMS immediately for last-minute Mindbody bookings, ensuring you never miss out on business opportunities.":
        "막바지 Mindbody 예약에 대해 이메일 또는 SMS로 Zoom 링크를 즉시 자동 전송하여, 비즈니스 기회를 놓치지 않도록 합니다.",
    "Automatically send thank-you emails, receipts, and follow-up messages based on donor actions and gift details - ensuring timely, consistent communication every time.":
        "기부자 활동과 기부 세부 정보를 기반으로 감사 이메일, 영수증, 후속 메시지를 자동 전송하여, 매번 적시의 일관된 커뮤니케이션을 보장합니다.",
    "Automatically share new and cancelled membership details from Mindbody with your connected apps to simplify onboarding, retention strategies, marketing outreach, and reporting.":
        "Mindbody의 신규 및 취소된 멤버십 세부 정보를 연결된 앱과 자동으로 공유하여, 온보딩, 유지 전략, 마케팅 아웃리치, 보고를 간소화합니다.",
    "Automatically sign in Zoom attendees to Mindbody after each class, eliminating manual check-ins for instructors.":
        "각 수업 후 Zoom 참석자를 Mindbody에 자동으로 체크인하여, 강사의 수동 체크인을 제거합니다.",
    "Automatically sync Cliniko case information as organized Salesforce objects. Gain visibility into key case details, milestones, session limits, and referral notes - all accessible alongside related appointments.":
        "Cliniko 케이스 정보를 정리된 Salesforce 오브젝트로 자동 동기화합니다. 주요 케이스 세부 정보, 마일스톤, 세션 제한, 의뢰 노트에 대한 가시성을 확보하며, 모두 관련 예약과 함께 접근할 수 있습니다.",
    "Automatically sync Mindbody client indexes - such as age range, client type (spa or gym), experience level, and more - directly into HubSpot. Easily segment your contacts based on these indexes, enabling targeted marketing, personalized engagement, and more effective client management.":
        "연령대, 고객 유형(스파 또는 헬스장), 경험 수준 등과 같은 Mindbody 고객 인덱스를 HubSpot에 직접 자동 동기화합니다. 이러한 인덱스를 기반으로 연락처를 쉽게 세그먼트하여, 타겟 마케팅, 개인화 참여, 더 효과적인 고객 관리를 가능하게 합니다.",
    "Automatically sync Mindbody indexes and custom fields directly into ActiveCampaign, enabling powerful segmentation and highly personalized campaigns.":
        "Mindbody 인덱스와 맞춤 필드를 ActiveCampaign에 직접 자동 동기화하여, 강력한 세그멘테이션과 고도로 개인화된 캠페인을 가능하게 합니다.",
    "Automatically sync Mindbody services as non-inventory items in Shopify, allowing your customers to conveniently select their preferred location for service fulfillment during checkout.":
        "Mindbody 서비스를 Shopify에서 비재고 항목으로 자동 동기화하여, 고객이 결제 시 서비스 이행을 위한 선호 지점을 편리하게 선택할 수 있도록 합니다.",
    "Automatically sync answers to custom questions asked in Calendly directly to custom fields or indexes in Mindbody, ensuring personalized and informed client interactions.":
        "Calendly에서 물어본 맞춤 질문에 대한 답변을 Mindbody의 맞춤 필드 또는 인덱스에 직접 자동 동기화하여, 개인화되고 정보에 기반한 고객 상호작용을 보장합니다.",
    "Automatically sync bookings, visits, cancellations, and purchases directly into each client's timeline, enabling precise and timely communication.":
        "예약, 방문, 취소, 구매를 각 고객의 타임라인에 직접 자동 동기화하여, 정확하고 적시의 커뮤니케이션을 가능하게 합니다.",
    "Automatically sync detailed Mindbody data into Zoho CRM custom objects - powering precise automations, insightful reporting, and targeted client experiences.":
        "상세 Mindbody 데이터를 Zoho CRM 맞춤 오브젝트에 자동 동기화하여, 정밀한 자동화, 통찰력 있는 보고, 타겟 고객 경험을 구동합니다.",
    "Automatically sync donor communication preferences and narrative fields to send timely thank-yous and personalized follow-ups.":
        "기부자 커뮤니케이션 선호도와 내러티브 필드를 자동 동기화하여, 적시 감사 메시지와 개인화 후속 조치를 전송합니다.",
    "Automatically sync email preferences such as \"Do Not Email\" from DonorPerfect, helping you maintain donor trust and compliance with communication preferences.":
        "DonorPerfect의 \"이메일 수신 거부\"와 같은 이메일 선호도를 자동 동기화하여, 기부자 신뢰와 커뮤니케이션 선호도 준수를 유지합니다.",
    "Automatically sync essential Mindbody client data to Klaviyo, powering personalized email and SMS automations for meaningful client interactions.":
        "필수 Mindbody 고객 데이터를 Klaviyo에 자동 동기화하여, 의미 있는 고객 상호작용을 위한 개인화 이메일 및 SMS 자동화를 구동합니다.",
    "Automatically sync essential patient details from Cliniko to ActiveCampaign, including appointment totals, lifetime value, patient notes, and referral information. Keep your contacts accurate and current without lifting a finger.":
        "예약 합계, 생애 가치, 환자 노트, 의뢰 정보를 포함한 필수 환자 세부 정보를 Cliniko에서 ActiveCampaign으로 자동 동기화합니다. 수고 없이 연락처를 정확하고 최신 상태로 유지합니다.",
    "Automatically sync new, updated, and canceled class bookings from Mindbody to Zapier, keeping your class schedules accurate and timely.":
        "Mindbody에서 Zapier로 신규, 업데이트, 취소된 수업 예약을 자동 동기화하여, 수업 일정을 정확하고 적시에 유지합니다.",
    "Automatically sync over 140 donor properties from DonorPerfect into HubSpot, including personal details, giving history, and preferences, allowing for tailored communications.":
        "개인 정보, 기부 이력, 선호도를 포함한 140개 이상의 기부자 속성을 DonorPerfect에서 HubSpot으로 자동 동기화하여, 맞춤 커뮤니케이션을 가능하게 합니다.",
    "Automatically sync your clients' most recent purchases - including intro offers, services, and products - directly into HubSpot. Leverage this data to automate personalized lead nurturing, create targeted newsletters, and build dynamic lists based on purchase history.":
        "체험 상품, 서비스, 제품을 포함한 고객의 최근 구매를 HubSpot에 직접 자동 동기화합니다. 이 데이터를 활용하여 개인화 리드 육성을 자동화하고, 타겟 뉴스레터를 작성하고, 구매 이력 기반 동적 목록을 구축합니다.",
    "Automatically synchronize patient and contact data, including demographics, preferences, and appointment history.":
        "인구통계, 선호도, 예약 이력을 포함한 환자 및 연락처 데이터를 자동으로 동기화합니다.",
    "Automatically tag clients based on which Mindbody locations they book, visit, or purchase at. Get a unified view across all your sites, ideal for franchises and multi-location operations.":
        "고객이 예약, 방문, 구매하는 Mindbody 지점을 기반으로 자동 태그를 지정합니다. 모든 사이트의 통합 뷰를 확보하며, 프랜차이즈 및 다중 지점 운영에 적합합니다.",
    "Automatically tag clients in HubSpot based on the specific Mindbody locations where they book, visit, or purchase. CRMConnect keeps each client's record consistently updated across all your sites, providing a unified view of client activity. This ensures clear segmentation, personalized communications, and valuable insights for multi-location or regional operations.":
        "고객이 예약, 방문, 구매하는 특정 Mindbody 지점을 기반으로 HubSpot에서 자동 태그를 지정합니다. CRMConnect는 모든 사이트에서 각 고객 기록을 일관되게 업데이트하여, 고객 활동의 통합 뷰를 제공합니다. 명확한 세그멘테이션, 개인화 커뮤니케이션, 다중 지점 또는 지역 운영을 위한 가치 있는 인사이트를 보장합니다.",
    "Automatically tag consultation appointments in Keap, helping your team quickly identify new client opportunities and trigger the right nurture sequences at the right time.":
        "Keap에서 상담 예약에 자동으로 태그를 지정하여, 팀이 신규 고객 기회를 신속하게 식별하고 적시에 적절한 육성 시퀀스를 트리거할 수 있도록 합니다.",
    "Automatically track all Cliniko appointments as custom Salesforce objects, categorized by status - Booked, Arrived, Did Not Arrive, or Cancelled. Sync telehealth URLs and enable automated follow-ups directly from Salesforce.":
        "모든 Cliniko 예약을 맞춤 Salesforce 오브젝트로 자동 추적하며, 상태별(예약됨, 도착, 미도착, 취소)로 분류합니다. 텔레헬스 URL을 동기화하고 Salesforce에서 직접 자동 후속 조치를 가능하게 합니다.",
    "Automatically track clients' most recent visits, empowering you to effectively follow up or proactively re-engage clients who haven't scheduled an appointment or class within a specified timeframe.":
        "고객의 최근 방문을 자동으로 추적하여, 지정된 기간 내에 예약이나 수업을 예약하지 않은 고객에 대한 효과적인 후속 조치 또는 사전 재참여를 가능하게 합니다.",
    "Automatically track clients' most recent visits, empowering you to follow up or proactively re-engage clients who haven't visited within a specified timeframe.":
        "고객의 최근 방문을 자동으로 추적하여, 지정된 기간 내에 방문하지 않은 고객에 대한 후속 조치 또는 사전 재참여를 가능하게 합니다.",
    "Automatically track each client's membership status, expiration dates, and remaining sessions to effortlessly manage renewals and upsells.":
        "각 고객의 멤버십 상태, 만료일, 잔여 세션을 자동으로 추적하여, 갱신과 업셀을 손쉽게 관리합니다.",
    "Automatically track each client's membership status, expiration dates, remaining sessions to effortlessly manage renewals and upsells.":
        "각 고객의 멤버십 상태, 만료일, 잔여 세션을 자동으로 추적하여, 갱신과 업셀을 손쉽게 관리합니다.",
    "Automatically transfer DonorPerfect flags as HubSpot multi-select tags for easy segmentation and simplified data management.":
        "DonorPerfect 플래그를 HubSpot 다중 선택 태그로 자동 전환하여, 쉬운 세그멘테이션과 간소화된 데이터 관리를 지원합니다.",
    "Automatically transfer dropdown menus like donor types and campaign codes from DonorPerfect to Mailchimp, ensuring consistent categorization across both systems.":
        "기부자 유형 및 캠페인 코드와 같은 드롭다운 메뉴를 DonorPerfect에서 Mailchimp으로 자동 전환하여, 두 시스템에서 일관된 분류를 보장합니다.",
    "Automatically turn Calendly bookings into Mindbody appointments, providing effortless, accurate scheduling and a superior client experience.":
        "Calendly 예약을 Mindbody 예약으로 자동 변환하여, 손쉽고 정확한 일정 관리와 우수한 고객 경험을 제공합니다.",
    "Automatically turn Cliniko data into actionable insights and automations within ActiveCampaign, streamlining your operations and enhancing patient relationships.":
        "Cliniko 데이터를 ActiveCampaign 내에서 실행 가능한 인사이트와 자동화로 자동 전환하여, 운영을 간소화하고 환자 관계를 강화합니다.",
    "Automatically turn Cliniko data into actionable insights and automations within HubSpot, streamlining your operations and enhancing patient relationships.":
        "Cliniko 데이터를 HubSpot 내에서 실행 가능한 인사이트와 자동화로 자동 전환하여, 운영을 간소화하고 환자 관계를 강화합니다.",
    "Automatically turn Cliniko data into actionable insights and workflows within Salesforce, streamlining your operations and enhancing patient relationships.":
        "Cliniko 데이터를 Salesforce 내에서 실행 가능한 인사이트와 워크플로우로 자동 전환하여, 운영을 간소화하고 환자 관계를 강화합니다.",
    "Automatically turn DonorPerfect data into actionable insights and automations within ActiveCampaign, streamlining your operations and strengthening donor relationships.":
        "DonorPerfect 데이터를 ActiveCampaign 내에서 실행 가능한 인사이트와 자동화로 자동 전환하여, 운영을 간소화하고 기부자 관계를 강화합니다.",
    "Automatically turn DonorPerfect data into actionable insights and automations within Keap, streamlining your operations and enhancing donor relationships.":
        "DonorPerfect 데이터를 Keap 내에서 실행 가능한 인사이트와 자동화로 자동 전환하여, 운영을 간소화하고 기부자 관계를 강화합니다.",
    "Automatically turn Mindbody data into actionable insights and automations within Keap, streamlining your operations and enhancing client relationships.":
        "Mindbody 데이터를 Keap 내에서 실행 가능한 인사이트와 자동화로 자동 전환하여, 운영을 간소화하고 고객 관계를 강화합니다.",
    "Automatically update ActiveCampaign contacts with accurate appointment details from Cliniko, including both individual and group sessions. Enable precise segmentation, targeted messaging, and efficient patient engagement.":
        "개별 및 그룹 세션을 포함한 Cliniko의 정확한 예약 세부 정보로 ActiveCampaign 연락처를 자동 업데이트합니다. 정밀한 세그멘테이션, 타겟 메시지, 효율적인 환자 참여를 가능하게 합니다.",
    "Automatically update ActiveCampaign contacts with the date and time of last appointment booked, last appointment completed, and location visited. Personalize communications and automate timely follow-ups effortlessly.":
        "마지막 예약일시, 마지막 완료 예약, 방문 지점으로 ActiveCampaign 연락처를 자동 업데이트합니다. 커뮤니케이션을 개인화하고 적시의 후속 조치를 손쉽게 자동화합니다.",
    "Automatically update ActiveCampaign deals with invoice data from Cliniko, including lifetime spend, latest invoice amount, and invoice number. Gain deeper insights into patient value and enable targeted follow-ups.":
        "생애 지출, 최근 인보이스 금액, 인보이스 번호를 포함한 Cliniko의 인보이스 데이터로 ActiveCampaign 거래를 자동 업데이트합니다. 환자 가치에 대한 더 깊은 인사이트를 얻고 타겟 후속 조치를 가능하게 합니다.",
    "Automatically update inventory after each sale on Shopify or Mindbody, with nightly reconciliations to accurately reflect replenishments made in Mindbody.":
        "Shopify 또는 Mindbody에서 판매할 때마다 재고를 자동 업데이트하며, 야간 조정으로 Mindbody에서 이루어진 보충을 정확하게 반영합니다.",
    "Automatically update upcoming, completed, and canceled appointments directly in Klaviyo, allowing for personalized messaging around scheduling and follow-ups.":
        "예정된, 완료된, 취소된 예약을 Klaviyo에 직접 자동 업데이트하여, 일정 및 후속 조치에 관한 개인화 메시지를 가능하게 합니다.",
    "Automation #4147": "Automation #4147",
    "Automation + Assembly editors": "Automation + Assembly 에디터",
    "Automation Editor": "Automation Editor",
    "Automation Editor | APIANT": "Automation Editor | APIANT",
    "Automation Editor | Visual. Powerful. Production-Grade.": "Automation Editor | 시각적. 강력함. 프로덕션 수준.",
    "Automation Editor: MindBody → HubSpot CRM Sync": "Automation Editor: MindBody → HubSpot CRM 동기화",
    "Automations": "자동화",
    "Autonomous Operations": "자율 운영",
    "Autonomous testing": "자율 테스트",
    "Average time to manually process a single DSAR": "단일 DSAR을 수동 처리하는 평균 시간",
    "Award-Winning Tech Support": "수상 경력의 기술 지원",
    "Award-Winning Technical Support": "수상 경력의 기술 지원",
    "Based on a real SaaS company conversation. The reaction from their DevRel lead: \"How do we make this happen?\"":
        "실제 SaaS 회사 대화를 기반으로 합니다. DevRel 리드의 반응: \"어떻게 하면 이것을 실현할 수 있나요?\"",
    "Based on the documentation, it recommends specific endpoints to build: \"Delete Task,\" \"Create Project,\" \"Update Assignment,\" and more.":
        "문서를 기반으로 구축할 특정 엔드포인트를 추천합니다: \"작업 삭제,\" \"프로젝트 생성,\" \"할당 업데이트\" 등.",
    "Based on what we found, here are integration products that might be a great fit.":
        "조사 결과를 바탕으로 적합한 통합 제품을 소개합니다.",
    "Basic AI features, no deep integration access": "기본 AI 기능, 심층 통합 접근 불가",
    "Batch Emails That Get Ignored": "무시되는 대량 이메일",
    "Battle-tested across every customer": "모든 고객에서 검증됨",
    "Before and after comparison: Shadow IT chaos with tangled connections versus centralized APIANT governance with clean routing":
        "이전/이후 비교: 엉킨 연결의 Shadow IT 혼란 vs. 깔끔한 라우팅의 중앙 집중식 APIANT 거버넌스",
    "Before you see pricing, see exactly what you're getting - and why hundreds of healthcare practices already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 수백 개의 의료 기관이 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting - and why hundreds of nonprofit organizations already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 수백 개의 비영리 단체가 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting - and why hundreds of wellness businesses already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 수백 개의 웰니스 비즈니스가 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting - and why wellness businesses already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 웰니스 비즈니스가 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting, and why hundreds of wellness businesses already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 수백 개의 웰니스 비즈니스가 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting, and why nonprofits already rely on it.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 비영리 단체가 이미 의존하는 이유를 알아보세요.",
    "Before you see pricing, see exactly what you're getting, and why wellness businesses trust ShopConnect to power their online sales.":
        "가격을 확인하기 전에, 정확히 무엇을 받게 되는지 확인하세요. 웰니스 비즈니스가 온라인 판매를 위해 ShopConnect를 신뢰하는 이유를 알아보세요.",
    "Behavioral Segmentation": "행동 기반 세그멘테이션",
    "Behavioral data": "행동 데이터",
    "Behavioral segmentation": "행동 기반 세그멘테이션",
    "Benefits": "혜택",
    "Best Practices:": "모범 사례:",
    "Best for: Enterprises that need deep integrations now and want to validate the platform before committing internal resources.":
        "적합 대상: 지금 심층 통합이 필요하고 내부 리소스를 투입하기 전에 플랫폼을 검증하려는 기업.",
    "Best for: Enterprises with integration-heavy operations that want long-term control and the ability to scale across departments.":
        "적합 대상: 통합 중심 운영을 하며 장기적인 제어와 부서 간 확장 능력을 원하는 기업.",
    "Best for: SaaS companies serious about integration as a long-term competitive advantage.":
        "적합 대상: 통합을 장기적 경쟁 우위로 진지하게 고려하는 SaaS 회사.",
    "Best for: SaaS companies that want integration solved immediately, or where six-figure franchise deals need integration as a differentiator today.":
        "적합 대상: 즉각적인 통합 해결을 원하는 SaaS 회사, 또는 6자리 프랜차이즈 계약에서 통합이 차별화 요소로 필요한 경우.",
    "Bi-Directional Client Sync": "양방향 고객 동기화",
    "Bi-Directional Contact Sync": "양방향 연락처 동기화",
    "Bi-Directional Patient Sync": "양방향 환자 동기화",
    "Bi-Directional Patient and Contact Sync": "양방향 환자 및 연락처 동기화",
    "Bi-directional sync with conflict resolution": "충돌 해결이 포함된 양방향 동기화",
    "Billing (Stripe)": "결제 (Stripe)",
    "Blog Posts": "블로그 게시물",
    "Bookings sync instantly.": "예약이 즉시 동기화됩니다.",
    "Brad B.": "Brad B.",
    "Branch based on settings: \"Does this customer use custom objects? Branch left for yes, right for no.\" \"Does this franchise track snowbird customers across locations? If yes, update the multi-location dropdown.\"":
        "설정에 따른 분기: \"이 고객이 맞춤 오브젝트를 사용하나요? 예이면 왼쪽, 아니오이면 오른쪽으로 분기.\" \"이 프랜차이즈가 지점 간 계절 이동 고객을 추적하나요? 예이면 다중 지점 드롭다운을 업데이트.\"",
    "Branding and UI preferences": "브랜딩 및 UI 선호 설정",
    "Breaks when APIs change": "API가 변경되면 중단됨",
    "Bridging The Divide Between Open APIs and Business Needs":
        "개방형 API와 비즈니스 요구 사이의 간극 해소",
    "Browse 500+ prebuilt connectors for the APIANT integration platform. Connect any app with deep, production-ready integrations.":
        "APIANT 통합 플랫폼을 위한 500개 이상의 사전 구축 커넥터를 둘러보세요. 심층적이고 프로덕션에 즉시 투입 가능한 통합으로 모든 앱을 연결하세요.",
    "Budget-Friendly, Impact-Heavy": "합리적인 비용, 높은 효과",
    "Build": "구축",
    "Build & Monetize": "구축 및 수익화",
    "Build 5 products": "5개 제품 구축",
    "Build AI chatbots that execute real workflows. APIANT chatbots query APIs, run automations, and take action across your entire tech stack.":
        "실제 워크플로우를 실행하는 AI 챗봇을 구축하세요. APIANT 챗봇은 API를 조회하고, 자동화를 실행하고, 전체 기술 스택에서 조치를 취합니다.",
    "Build AI chatbots that execute real workflows. APIANT chatbots query APIs, run automations, and take action across your entire tech stack. See a GDPR compliance chatbot in action.":
        "실제 워크플로우를 실행하는 AI 챗봇을 구축하세요. APIANT 챗봇은 API를 조회하고, 자동화를 실행하고, 전체 기술 스택에서 조치를 취합니다. GDPR 컴플라이언스 챗봇의 실제 동작을 확인하세요.",
    "Build AI-powered UIs that connect directly to the APIANT automation engine. Make integration invisible.":
        "APIANT 자동화 엔진에 직접 연결되는 AI 기반 UI를 구축하세요. 통합을 보이지 않게 만드세요.",
    "Build AI-powered, logic-driven UIs embeddable anywhere. FormApps connect directly to the APIANT automation engine - your end users never see APIANT.":
        "어디서나 임베드 가능한 AI 기반, 로직 중심 UI를 구축하세요. FormApps는 APIANT 자동화 엔진에 직접 연결되며, 최종 사용자는 APIANT를 볼 수 없습니다.",
    "Build AI-powered, logic-driven UIs that connect directly to the APIANT automation engine. Your end users never see APIANT. They see your product.":
        "APIANT 자동화 엔진에 직접 연결되는 AI 기반, 로직 중심 UI를 구축하세요. 최종 사용자는 APIANT를 볼 수 없습니다. 여러분의 제품을 봅니다.",
    "Build ActiveCampaign automations on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 ActiveCampaign 자동화를 구축하세요. 중요한 것을 자동화하세요.",
    "Build ActiveCampaign automations on rich, real-time donor data. Automate what matters.":
        "풍부한 실시간 기부자 데이터로 ActiveCampaign 자동화를 구축하세요. 중요한 것을 자동화하세요.",
    "Build ActiveCampaign automations on rich, real-time patient data. Automate what matters.":
        "풍부한 실시간 환자 데이터로 ActiveCampaign 자동화를 구축하세요. 중요한 것을 자동화하세요.",
    "Build Any UI. Embed It Anywhere.": "모든 UI를 구축하세요. 어디서나 임베드하세요.",
    "Build Any UI. Wire Any Logic.": "모든 UI를 구축하세요. 모든 로직을 연결하세요.",
    "Build Chatbots That Act,": "행동하는 챗봇을 구축하세요,",
    "Build Connectors While You Sleep": "잠자는 동안 커넥터를 구축하세요",
    "Build HighLevel workflows on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 HighLevel 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build HubSpot workflows on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 HubSpot 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build HubSpot workflows on rich, real-time donor data. Automate what matters.":
        "풍부한 실시간 기부자 데이터로 HubSpot 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build HubSpot workflows on rich, real-time patient data. Automate what matters.":
        "풍부한 실시간 환자 데이터로 HubSpot 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build In-House": "자체 구축",
    "Build Keap automations on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 Keap 자동화를 구축하세요. 중요한 것을 자동화하세요.",
    "Build Keap automations on rich, real-time donor data. Automate what matters.":
        "풍부한 실시간 기부자 데이터로 Keap 자동화를 구축하세요. 중요한 것을 자동화하세요.",
    "Build Klaviyo flows on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 Klaviyo 플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build Mailchimp campaigns on rich, up-to-date donor data. Send the right message to the right donors.":
        "풍부한 최신 기부자 데이터로 Mailchimp 캠페인을 구축하세요. 적절한 기부자에게 적절한 메시지를 전송하세요.",
    "Build Once. Deploy to Hundreds. Let Each Customer Consume It Differently.":
        "한 번 구축. 수백 곳에 배포. 각 고객이 다르게 사용하도록.",
    "Build Salesforce workflows on rich, real-time patient data. Automate what matters.":
        "풍부한 실시간 환자 데이터로 Salesforce 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build Your First Chatbot": "첫 번째 챗봇을 구축하세요",
    "Build Zapier workflows on rich, real-time Mindbody data. Connect to 5,000+ apps and automate what matters.":
        "풍부한 실시간 Mindbody 데이터로 Zapier 워크플로우를 구축하세요. 5,000개 이상의 앱에 연결하고 중요한 것을 자동화하세요.",
    "Build Zoho CRM workflows on rich, real-time client data. Automate what matters.":
        "풍부한 실시간 고객 데이터로 Zoho CRM 워크플로우를 구축하세요. 중요한 것을 자동화하세요.",
    "Build connectors for niche verticals in hours, not months. Productize integrations the big platforms ignore.":
        "니치 버티컬을 위한 커넥터를 몇 달이 아닌 몇 시간 만에 구축하세요. 대형 플랫폼이 무시하는 통합을 제품화하세요.",
    "Build deep integrations visually. Conditional branching, error handling, rate limiting, real-time monitoring. One codebase serves hundreds of customers.":
        "심층 통합을 시각적으로 구축하세요. 조건부 분기, 오류 처리, 속도 제한, 실시간 모니터링. 하나의 코드베이스가 수백 명의 고객에게 서비스합니다.",
    "Build deep integrations with real business logic (conditional routing, data transformation, error handling, retry logic) using visual tools, not code.":
        "코드가 아닌 시각적 도구를 사용하여 실제 비즈니스 로직(조건부 라우팅, 데이터 변환, 오류 처리, 재시도 로직)이 포함된 심층 통합을 구축하세요.",
    "Build intelligent intake forms that use AI to auto-complete fields, validate data, and trigger complex automations the moment a form is submitted. Not a static form. A smart one.":
        "AI를 사용하여 필드를 자동 완성하고, 데이터를 검증하고, 양식 제출 즉시 복잡한 자동화를 트리거하는 지능형 접수 양식을 구축하세요. 정적 양식이 아닙니다. 스마트한 양식입니다.",
    "Build interfaces visually. Arrange fields, sections, and components without writing code.":
        "인터페이스를 시각적으로 구축하세요. 코드 작성 없이 필드, 섹션, 구성요소를 배치하세요.",
    "Build me a \"Delete Task\" action for Asana": "Asana용 \"작업 삭제\" 액션을 구축해 주세요",
    "Build once, deploy to hundreds": "한 번 구축, 수백 곳에 배포",
    "Build one integration product. Price it at $99/month. Watch what happens.":
        "통합 제품 하나를 구축하세요. $99/월로 가격을 책정하세요. 무슨 일이 일어나는지 지켜보세요.",
    "Build your first integration in minutes with the AI Co-Pilot.":
        "AI Co-Pilot으로 몇 분 만에 첫 번째 통합을 구축하세요.",
    "Building connection assembly…": "연결 assembly 구축 중...",
    "Building \"Delete Task\" action…": "\"작업 삭제\" 액션 구축 중...",
    "Builds every endpoint": "모든 엔드포인트를 구축합니다",
    "Built Different at the Core": "핵심부터 다르게 구축됨",
    "Built for Compliance. Secured by Design.": "컴플라이언스를 위해 구축. 설계부터 보안.",
    "Built for Enterprise Complexity": "기업의 복잡성을 위해 구축됨",
    "Built-In Error Handling and Retry Logic": "내장된 오류 처리 및 재시도 로직",
    "Built-in": "내장",
    "Built-in error handling, retry logic, data validation, rate limiting":
        "내장된 오류 처리, 재시도 로직, 데이터 검증, 속도 제한",
    "Built-in handling of fitness-specific scenarios like class packages, memberships, and multi-location management":
        "수업 패키지, 멤버십, 다중 지점 관리와 같은 피트니스 특화 시나리오의 내장 처리",
    "Built-in handling of healthcare-specific scenarios like patient records, treatment notes, invoices, and multi-practitioner management":
        "환자 기록, 치료 노트, 인보이스, 다중 실무자 관리와 같은 의료 특화 시나리오의 내장 처리",
    "Built-in handling of nonprofit-specific scenarios like donor segments, gift types, campaigns, and multi-fund management":
        "기부자 세그먼트, 기부 유형, 캠페인, 다중 펀드 관리와 같은 비영리 특화 시나리오의 내장 처리",
    "Built-in monitoring lets you answer customer questions in seconds, not hours.":
        "내장 모니터링으로 고객 질문에 몇 시간이 아닌 몇 초 만에 답변할 수 있습니다.",
    "Bulk Deployment": "대량 배포",
    "Business Impact": "비즈니스 효과",
    "Business Location Sync": "비즈니스 지점 동기화",
    "Business integration that mirrors your entire Mindbody operation in ZohoCRM. All business objects - clients, sales, payments, services, memberships, and contracts - are automatically synchronized in real-time, enabling unified management across multiple locations.":
        "전체 Mindbody 운영을 ZohoCRM에 미러링하는 비즈니스 통합. 모든 비즈니스 오브젝트(고객, 판매, 결제, 서비스, 멤버십, 계약)가 실시간으로 자동 동기화되어, 다중 지점의 통합 관리를 가능하게 합니다.",
    "By default, appointments load 7 days back and 30 days forward; visits and sales load 1 month back. More history can be added for a small Mindbody API fee.":
        "기본적으로 예약은 과거 7일, 미래 30일까지 로드되며, 방문과 판매는 과거 1개월까지 로드됩니다. 소액의 Mindbody API 비용으로 추가 이력을 로드할 수 있습니다.",
    "By default, appointments sync 7 days back and 30 days forward; sales and visits sync 1 month back. Additional historical data can be imported upon request.":
        "기본적으로 예약은 과거 7일, 미래 30일까지 동기화되며, 판매와 방문은 과거 1개월까지 동기화됩니다. 요청 시 추가 이력 데이터를 가져올 수 있습니다.",
    "CRM (HubSpot)": "CRM (HubSpot)",
    "CRM and automation for allied health practices": "보건 의료 실무를 위한 CRM 및 자동화",
    "CRM and automation for nonprofits and fundraising": "비영리 단체 및 모금을 위한 CRM 및 자동화",
    "CRM connection shared across all locations": "모든 지점에서 공유되는 CRM 연결",
    "CRM sync, e-commerce, calendars, video, email marketing, and more for fitness studios and wellness businesses.":
        "피트니스 스튜디오 및 웰니스 비즈니스를 위한 CRM 동기화, 이커머스, 캘린더, 비디오, 이메일 마케팅 등.",
    "CRM, e-commerce, calendar, and more for fitness and wellness":
        "피트니스 및 웰니스를 위한 CRM, 이커머스, 캘린더 등",
    "CRMCONNECT Cliniko and ActiveCampaign": "CRMCONNECT Cliniko 및 ActiveCampaign",
    "CRMConnect automatically creates and syncs over 120 custom HubSpot properties, specifically chosen to capture essential Mindbody client data points relevant to your wellness business.":
        "CRMConnect는 웰니스 비즈니스에 관련된 필수 Mindbody 고객 데이터 포인트를 캡처하기 위해 특별히 선택된 120개 이상의 맞춤 HubSpot 속성을 자동으로 생성하고 동기화합니다.",
    "CRMConnect automatically creates and syncs over 120 custom HubSpot properties, specifically chosen to capture essential Mindbody client data. Enable precise segmentation, targeted communication, and effective engagement.":
        "CRMConnect는 필수 Mindbody 고객 데이터를 캡처하기 위해 특별히 선택된 120개 이상의 맞춤 HubSpot 속성을 자동으로 생성하고 동기화합니다. 정밀한 세그멘테이션, 타겟 커뮤니케이션, 효과적인 참여를 가능하게 합니다.",
    "CRMConnect automatically creates essential Mindbody data fields in Keap during setup, ensuring precise client data tracking from day one - no manual configuration required.":
        "CRMConnect는 설정 시 Keap에 필수 Mindbody 데이터 필드를 자동으로 생성하여, 첫날부터 정밀한 고객 데이터 추적을 보장합니다. 수동 구성이 필요 없습니다.",
    "CRMConnect bridges Cliniko and ActiveCampaign, providing a unified platform to manage patient information and client relationships efficiently.":
        "CRMConnect는 Cliniko와 ActiveCampaign을 연결하여, 환자 정보와 고객 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Cliniko and ActiveCampaign, providing a unified platform to manage patient information and relationships efficiently.":
        "CRMConnect는 Cliniko와 ActiveCampaign을 연결하여, 환자 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Cliniko and HubSpot, providing a unified platform to manage patient information and client relationships efficiently.":
        "CRMConnect는 Cliniko와 HubSpot을 연결하여, 환자 정보와 고객 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Cliniko and Salesforce, providing a unified platform to manage patient information and client relationships efficiently.":
        "CRMConnect는 Cliniko와 Salesforce를 연결하여, 환자 정보와 고객 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges DonorPerfect and ActiveCampaign, providing a unified platform to manage donor information and relationships efficiently.":
        "CRMConnect는 DonorPerfect와 ActiveCampaign을 연결하여, 기부자 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges DonorPerfect and HubSpot, providing a unified platform to automate your growth.":
        "CRMConnect는 DonorPerfect와 HubSpot을 연결하여, 성장을 자동화하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges DonorPerfect and HubSpot, providing a unified platform to manage donor information and relationships efficiently.":
        "CRMConnect는 DonorPerfect와 HubSpot을 연결하여, 기부자 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges DonorPerfect and Keap, providing a unified platform to manage donor information and relationships efficiently.":
        "CRMConnect는 DonorPerfect와 Keap을 연결하여, 기부자 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and ActiveCampaign, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 ActiveCampaign을 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and HighLevel, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 HighLevel을 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and HubSpot, providing a unified platform to automate your growth.":
        "CRMConnect는 Mindbody와 HubSpot을 연결하여, 성장을 자동화하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and HubSpot, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 HubSpot을 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and Keap, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 Keap을 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and Klaviyo, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 Klaviyo를 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect bridges Mindbody and Zoho CRM, providing a unified platform to manage client information and relationships efficiently.":
        "CRMConnect는 Mindbody와 Zoho CRM을 연결하여, 고객 정보와 관계를 효율적으로 관리하는 통합 플랫폼을 제공합니다.",
    "CRMConnect creates and maintains a dedicated Mindbody Appointment Pipeline in HubSpot, automatically representing each appointment as a deal.":
        "CRMConnect는 HubSpot에서 전용 Mindbody 예약 파이프라인을 생성하고 유지하며, 각 예약을 자동으로 거래로 표현합니다.",
    "CRMConnect keeps HubSpot updated with each client's most recent visit details - including date, type (appointment, class, or arrival), service provided, staff member, and event name.":
        "CRMConnect는 날짜, 유형(예약, 수업, 도착), 제공된 서비스, 담당 직원, 이벤트 이름을 포함한 각 고객의 최근 방문 세부 정보로 HubSpot을 최신 상태로 유지합니다.",
    "CRMConnect keeps HubSpot updated with each client's next scheduled appointment from Mindbody.":
        "CRMConnect는 Mindbody의 각 고객 다음 예약으로 HubSpot을 최신 상태로 유지합니다.",
    "CRMConnect only manages data syncing; automations are created and managed by you directly in Keap. Assistance is available through Keap experts if needed.":
        "CRMConnect는 데이터 동기화만 관리합니다. 자동화는 Keap에서 직접 생성하고 관리합니다. 필요 시 Keap 전문가를 통한 지원이 가능합니다.",
    "CRMConnect only syncs data. You build the automations. Need help? We can refer you to an ActiveCampaign partner.":
        "CRMConnect는 데이터만 동기화합니다. 자동화는 직접 구축합니다. 도움이 필요하면 ActiveCampaign 파트너를 소개해 드립니다.",
    "CRMConnect provides instant patient and contact updates from Salesforce to Cliniko using real-time webhooks. Updates from Cliniko back to Salesforce run automatically every 15 minutes. Advanced matching and deduplication algorithms ensure accurate, seamless syncing - keeping your patient and contact records consistently up-to-date across both systems.":
        "CRMConnect는 실시간 webhook을 사용하여 Salesforce에서 Cliniko로 즉각적인 환자 및 연락처 업데이트를 제공합니다. Cliniko에서 Salesforce로의 업데이트는 15분마다 자동으로 실행됩니다. 고급 매칭 및 중복 제거 알고리즘이 정확하고 원활한 동기화를 보장하여, 두 시스템에서 환자 및 연락처 기록을 일관되게 최신 상태로 유지합니다.",
    "CRMConnect provides the synced data. You build the automations within Klaviyo.":
        "CRMConnect가 동기화된 데이터를 제공합니다. Klaviyo 내에서 자동화를 구축합니다.",
    "CRMConnect provides the synced data. You configure automations, workflows, and reports inside Zoho CRM. Assistance available via integration partners if needed.":
        "CRMConnect가 동기화된 데이터를 제공합니다. Zoho CRM 내에서 자동화, 워크플로우, 보고서를 구성합니다. 필요 시 통합 파트너를 통한 지원이 가능합니다.",
    "CRMConnect relies on the \"Pays for\" and \"Is paid for\" relationship in Mindbody to identify family members and add them to the same company.":
        "CRMConnect는 Mindbody의 \"지불 대상\" 및 \"지불 받는 대상\" 관계를 사용하여 가족 구성원을 식별하고 동일한 회사에 추가합니다.",
    "CRMConnect requires Zoho CRM Enterprise or higher for optimal custom object management and advanced automation capabilities.":
        "CRMConnect는 최적의 맞춤 오브젝트 관리 및 고급 자동화 기능을 위해 Zoho CRM Enterprise 이상이 필요합니다.",
    "CRMConnect solves a major challenge for Mindbody businesses syncing with HubSpot: family members who share a single email address are automatically grouped together in HubSpot under a single company record.":
        "CRMConnect는 HubSpot과 동기화하는 Mindbody 비즈니스의 주요 과제를 해결합니다. 단일 이메일 주소를 공유하는 가족 구성원이 HubSpot에서 하나의 회사 레코드 아래에 자동으로 그룹화됩니다.",
    "CRMConnect syncs data to Keap. Automations and workflows are configured by you within Keap.":
        "CRMConnect가 Keap으로 데이터를 동기화합니다. 자동화와 워크플로우는 Keap 내에서 직접 구성합니다.",
    "CRMConnect syncs your clients' upcoming class bookings directly into HubSpot, providing clear visibility into their next scheduled visits.":
        "CRMConnect는 고객의 다가오는 수업 예약을 HubSpot에 직접 동기화하여, 다음 예정 방문에 대한 명확한 가시성을 제공합니다.",
    "CRMConnect was built to scale and can be customized to add any logic or additional apps you need to connect for the specific needs of your enterprise.":
        "CRMConnect는 확장을 위해 구축되었으며, 기업의 특정 요구사항을 위해 필요한 로직이나 추가 앱을 연결하도록 맞춤 설정할 수 있습니다.",
    "CRMConnect will work with the free version of HubSpot, but some features and benefits, such as Appointment and Sales pipeline require a HubSpot Pro Hub which also allows workflows. To set up even more powerful automations, a subscription to HubSpot's Sales Hub Enterprise allows for auto-enrolling contacts in sequences. This is one of the most powerful features CRMConnect enables.":
        "CRMConnect는 HubSpot 무료 버전에서도 작동하지만, 예약 및 판매 파이프라인과 같은 일부 기능은 워크플로우도 허용하는 HubSpot Pro Hub이 필요합니다. 더 강력한 자동화를 설정하려면, HubSpot Sales Hub Enterprise 구독이 시퀀스에 연락처를 자동 등록하는 것을 허용합니다. 이것은 CRMConnect가 가능하게 하는 가장 강력한 기능 중 하나입니다.",
    "CRMConnect will work with the free version of HubSpot, but some features and benefits, such as the Mindbody Appointment and Sales pipeline require a HubSpot Pro Hub which also allows workflows. To set up even more powerful automations, a subscription to HubSpot's Sales Hub Enterprise allows for auto-enrolling contacts in sequences. This is one of the most powerful features CRMConnect enables.":
        "CRMConnect는 HubSpot 무료 버전에서도 작동하지만, Mindbody 예약 및 판매 파이프라인과 같은 일부 기능은 워크플로우도 허용하는 HubSpot Pro Hub이 필요합니다. 더 강력한 자동화를 설정하려면, HubSpot Sales Hub Enterprise 구독이 시퀀스에 연락처를 자동 등록하는 것을 허용합니다. 이것은 CRMConnect가 가능하게 하는 가장 강력한 기능 중 하나입니다.",
    "CRMConnect works on all Klaviyo plans. SMS automations require Klaviyo SMS enabled.":
        "CRMConnect는 모든 Klaviyo 플랜에서 작동합니다. SMS 자동화에는 Klaviyo SMS 활성화가 필요합니다.",
    "CRMConnect works seamlessly with any paid Keap subscription.":
        "CRMConnect는 모든 유료 Keap 구독에서 원활하게 작동합니다.",
    "CRMConnect works with HubSpot Free, but features like the Gifts Pipeline and advanced automation require HubSpot Pro or Enterprise plans.":
        "CRMConnect는 HubSpot Free에서 작동하지만, Gifts Pipeline 및 고급 자동화와 같은 기능에는 HubSpot Pro 또는 Enterprise 플랜이 필요합니다.",
    "CRMConnect works with all Keap plans. Advanced automations may require higher-tier plans.":
        "CRMConnect는 모든 Keap 플랜에서 작동합니다. 고급 자동화에는 상위 플랜이 필요할 수 있습니다.",
    "CRMConnect: Master Account": "CRMConnect: 마스터 계정",
    "CX Apps in Partner Platforms": "파트너 플랫폼의 CX 앱",
    "Calculate Your Integration Business Margins": "통합 비즈니스 마진을 계산하세요",
    "CalendarConnect bridges Mindbody and Calendly, providing a unified platform to manage your bookings.":
        "CalendarConnect는 Mindbody와 Calendly를 연결하여, 예약을 관리하는 통합 플랫폼을 제공합니다.",
    "CalendarConnect Mindbody and Calendly": "CalendarConnect Mindbody 및 Calendly",
    "Calendly Question Sync": "Calendly 질문 동기화",
    "Calendly and Mindbody don't talk to each other, so the same time slot gets booked twice - frustrating clients and costing you revenue.":
        "Calendly와 Mindbody는 서로 통신하지 않으므로, 같은 시간대가 이중 예약됩니다. 고객에게 불편을 주고 매출 손실을 초래합니다.",
    "Campaign Performance Insights": "캠페인 성과 인사이트",
    "Campaign Performance Tracking": "캠페인 성과 추적",
    "Can AppConnect handle multiple Mindbody locations or accounts?": "AppConnect가 여러 Mindbody 지점이나 계정을 처리할 수 있나요?",
    "Can I choose when data syncing happens?": "데이터 동기화 시점을 선택할 수 있나요?",
    "Can I choose which donor information gets synced?": "어떤 기부자 정보가 동기화되는지 선택할 수 있나요?",
    "Can I connect more than one Mindbody location?": "하나 이상의 Mindbody 지점을 연결할 수 있나요?",
    "Can I customize the button color in the email?": "이메일에서 버튼 색상을 맞춤 설정할 수 있나요?",
    "Can I customize the email with my own text?": "이메일에 자체 텍스트로 맞춤 설정할 수 있나요?",
    "Can I customize the timing of Zoom meeting creation and notification emails?": "Zoom 미팅 생성 및 알림 이메일 시점을 맞춤 설정할 수 있나요?",
    "Can I have more than 500 products in Shopify?": "Shopify에 500개 이상의 제품을 등록할 수 있나요?",
    "Can I manage multiple Mindbody locations?": "여러 Mindbody 지점을 관리할 수 있나요?",
    "Can I process more than 1000 bookings per month?": "월 1000건 이상의 예약을 처리할 수 있나요?",
    "Can I sell products, services and packages in Shopify?": "Shopify에서 제품, 서비스, 패키지를 판매할 수 있나요?",
    "Can I send Zoom recordings to clients who missed the class?": "수업을 놓친 고객에게 Zoom 녹화 영상을 보낼 수 있나요?",
    "Can I start with Sandbox and upgrade later?": "Sandbox로 시작하고 나중에 업그레이드할 수 있나요?",
    "Can I sync custom fields from DonorPerfect?": "DonorPerfect에서 맞춤 필드를 동기화할 수 있나요?",
    "Can I sync more than 15 donor fields?": "15개 이상의 기부자 필드를 동기화할 수 있나요?",
    "Can I sync multiple Calendly event types?": "여러 Calendly 이벤트 유형을 동기화할 수 있나요?",
    "Can I sync multiple Mindbody locations and site ids to one HighLevel account?": "여러 Mindbody 지점과 사이트 ID를 하나의 HighLevel 계정에 동기화할 수 있나요?",
    "Can I track marketing ROI in Keap?": "Keap에서 마케팅 ROI를 추적할 수 있나요?",
    "Can I track marketing ROI in Zoho CRM?": "Zoho CRM에서 마케팅 ROI를 추적할 수 있나요?",
    "Can I track the success of specific fundraising campaigns?": "특정 모금 캠페인의 성과를 추적할 수 있나요?",
    "Can I use AppConnect with Zapier's free plan?": "Zapier 무료 플랜으로 AppConnect를 사용할 수 있나요?",
    "Can instructors receive their own Zoom start links?": "강사가 자체 Zoom 시작 링크를 받을 수 있나요?",
    "Can multiple Mindbody locations sync into a single Klaviyo account?": "여러 Mindbody 지점이 하나의 Klaviyo 계정에 동기화할 수 있나요?",
    "Can multiple Mindbody locations sync to one Zoho CRM account?": "여러 Mindbody 지점이 하나의 Zoho CRM 계정에 동기화할 수 있나요?",
    "Can multiple locations sync to one Keap account?": "여러 지점이 하나의 Keap 계정에 동기화할 수 있나요?",
    "Cancellation & Reschedule Sync": "취소 및 일정 변경 동기화",
    "Cancelled appointment booking": "취소된 예약",
    "Cancelled class booking": "취소된 수업 예약",
    "Cancelled class schedule": "취소된 수업 일정",
    "Cancelled client (instant)": "취소된 고객 (즉시)",
    "Cancelled membership": "취소된 멤버십",
    "Can't find the answer you're looking for? Please chat to our friendly team.":
        "원하는 답변을 찾을 수 없나요? 친절한 팀에 문의해 주세요.",
    "Capabilities": "기능",
    "Capability": "기능",
    "Capability scan": "기능 스캔",
    "Capture all Mindbody sales data, client services, and memberships within dedicated HighLevel custom objects for detailed financial analysis, precise tracking, and improved sales management.":
        "전용 HighLevel 맞춤 오브젝트에서 모든 Mindbody 판매 데이터, 고객 서비스, 멤버십을 캡처하여, 상세 재무 분석, 정밀 추적, 향상된 판매 관리를 제공합니다.",
    "Case & invoice sync": "케이스 및 인보이스 동기화",
    "Case Information Sync": "케이스 정보 동기화",
    "Case Studies": "사례 연구",
    "Case data sync": "케이스 데이터 동기화",
    "Catalog check": "카탈로그 확인",
    "Centralized Franchise Management": "중앙 집중식 프랜차이즈 관리",
    "Centralized control over users, automations, connections, and deployments. Role-based access controls. System monitoring and usage analytics. Manage hundreds of accounts from a single dashboard.":
        "사용자, 자동화, 연결, 배포에 대한 중앙 집중식 제어. 역할 기반 접근 제어. 시스템 모니터링 및 사용 분석. 단일 대시보드에서 수백 개의 계정을 관리합니다.",
    "Chat interaction triggering automation behind the scenes": "백그라운드에서 자동화를 트리거하는 채팅 상호작용",
    "Chat interactions that trigger complex multi-step automations spanning multiple platforms behind the scenes.":
        "백그라운드에서 여러 플랫폼에 걸친 복잡한 다단계 자동화를 트리거하는 채팅 상호작용.",
    "Chatbot": "챗봇",
    "Chatbot flow: user asks a question, automation engine processes through intent, API query, and formatting, returns structured response":
        "챗봇 흐름: 사용자가 질문하면, 자동화 엔진이 의도, API 조회, 포맷팅을 처리하고, 구조화된 응답을 반환",
    "Cheap per workflow, but costs multiply and quality suffers": "워크플로우당 비용은 저렴하지만, 비용이 증가하고 품질이 저하됨",
    "Check Your Inbox": "받은 편지함을 확인하세요",
    "Checkbox": "체크박스",
    "Checkboxes, dropdowns, multi-selects, all driven by the integration logic in the Automation Editor. No re-building.":
        "체크박스, 드롭다운, 다중 선택, 모두 Automation Editor의 통합 로직으로 구동됩니다. 재구축이 필요 없습니다.",
    "Child accounts managed from one master": "하나의 마스터에서 관리되는 하위 계정",
    "Child: Site 12": "하위: 사이트 12",
    "Child: Site 203": "하위: 사이트 203",
    "Child: Site 47": "하위: 사이트 47",
    "Choose exactly which Mindbody sale items - products, services, tips, account payments, or none - are synced into Shopify, giving you precise control over your sales data.":
        "제품, 서비스, 팁, 계정 결제 등 Shopify에 동기화할 Mindbody 판매 항목을 정확히 선택하여, 판매 데이터를 정밀하게 제어합니다.",
    "Choose the Data You Need": "필요한 데이터를 선택하세요",
    "Choose what to sync. CRMConnect handles the data logic, deduplication, and mapping.":
        "동기화할 항목을 선택하세요. CRMConnect가 데이터 로직, 중복 제거, 매핑을 처리합니다.",
    "Choose which appointments get Zoom links. ZoomConnect handles creation, distribution, and tracking.":
        "Zoom 링크를 받을 예약을 선택하세요. ZoomConnect가 생성, 배포, 추적을 처리합니다.",
    "Choose which connectors to activate. AppConnect handles the data enrichment, webhook delivery, and payload formatting.":
        "활성화할 커넥터를 선택하세요. AppConnect가 데이터 보강, webhook 전달, payload 포맷팅을 처리합니다.",
    "Choose which donor fields, filters, and flags to sync. MailConnect handles the data logic and mapping.":
        "동기화할 기부자 필드, 필터, 플래그를 선택하세요. MailConnect가 데이터 로직과 매핑을 처리합니다.",
    "Choose which event types to sync. CalendarConnect handles the scheduling logic, client matching, and data mapping.":
        "동기화할 이벤트 유형을 선택하세요. CalendarConnect가 일정 로직, 고객 매칭, 데이터 매핑을 처리합니다.",
    "Choose which products, services, and inventory to sync. ShopConnect handles pricing, taxes, and variants automatically.":
        "동기화할 제품, 서비스, 재고를 선택하세요. ShopConnect가 가격, 세금, 변형을 자동으로 처리합니다.",
    "Christophe B.": "Christophe B.",
    "Class & Appointment Calendar Sync": "수업 및 예약 캘린더 동기화",
    "Class & Appointment Pack Tracking": "수업 및 예약 패키지 추적",
    "Class Booking & Schedule Management": "수업 예약 및 일정 관리",
    "Class Booking Management": "수업 예약 관리",
    "Class Booking Sync": "수업 예약 동기화",
    "Class Pack Tracking & Automation": "수업 패키지 추적 및 자동화",
    "Class Schedule Management": "수업 일정 관리",
    "Class Schedule Sync": "수업 일정 동기화",
    "Class Sync & Attendance Tracking": "수업 동기화 및 출석 추적",
    "Class Sync and Attendance Tracking": "수업 동기화 및 출석 추적",
    "Class and Appointment Calendar Sync": "수업 및 예약 캘린더 동기화",
    "Class updated (instant)": "수업 업데이트됨 (즉시)",
    "Classes > HL Calendar": "수업 > HL 캘린더",
    "Cleaned Address Management": "정리된 주소 관리",
    "Clear Fundraising Insights": "명확한 모금 인사이트",
    "Clear Fundraising Insights and Reports": "명확한 모금 인사이트 및 보고서",
    "Clear Fundraising Insights with the Gifts Pipeline add-on": "Gifts Pipeline 애드온을 통한 명확한 모금 인사이트",
    "Clear Fundraising Metrics": "명확한 모금 지표",
    "Clear deal property": "거래 속성 지우기",
    "Clearly link client payments and purchases to services, campaigns, and locations.":
        "고객 결제와 구매를 서비스, 캠페인, 지점에 명확하게 연결합니다.",
    "Clearly track how your marketing efforts influence donations, letting you see exactly which strategies bring in the most money - so you can spend your advertising budget wisely and effectively.":
        "마케팅 노력이 기부에 어떤 영향을 미치는지 명확하게 추적하여, 어떤 전략이 가장 많은 기부금을 유치하는지 정확히 파악하고, 광고 예산을 현명하고 효과적으로 사용할 수 있습니다.",
    "Clearly track your clients' appointment packs - including remaining session counts - in HubSpot. Use this data to build automated workflows that proactively prompt clients to replenish sessions, ensuring continuous engagement and preventing gaps in service.":
        "HubSpot에서 잔여 세션 수를 포함한 고객의 예약 패키지를 명확하게 추적합니다. 이 데이터를 사용하여 고객에게 세션 보충을 사전에 안내하는 자동화 워크플로우를 구축하여, 지속적인 참여를 보장하고 서비스 중단을 방지합니다.",
    "Click the button below to start talking. Alex already has your details.":
        "아래 버튼을 클릭하여 대화를 시작하세요. Alex가 이미 귀하의 세부 정보를 가지고 있습니다.",
    "Click to access detailed documentation of data payloads for each connector.":
        "각 커넥터의 데이터 payload에 대한 상세 문서에 접근하려면 클릭하세요.",
    "Client Contract Management": "고객 계약 관리",
    "Client Data Auto-Sync": "고객 데이터 자동 동기화",
    "Client Index & Custom Field Sync": "고객 인덱스 및 맞춤 필드 동기화",
    "Client Index Sync": "고객 인덱스 동기화",
    "Client Management": "고객 관리",
    "Client Management (New/Updated/Deactivated)": "고객 관리 (신규/업데이트/비활성화)",
    "Client Purchase History Sync": "고객 구매 이력 동기화",
    "Client Services > HL Custom Object": "고객 서비스 > HL 맞춤 오브젝트",
    "Client Services > HighLevel Custom Object": "고객 서비스 > HighLevel 맞춤 오브젝트",
    "Client Services Custom Object": "고객 서비스 맞춤 오브젝트",
    "Client Services Sync": "고객 서비스 동기화",
    "Client and contact syncing happens instantly. Sales, class bookings, appointment bookings, membership, and contract info synced from Mindbody to the HubSpot contact also occur instantly. The Mindbody Appointment Pipeline is updated every 15 mins. Visits and the Mindbody Sales Pipeline are updated once a day.":
        "고객 및 연락처 동기화는 즉시 이루어집니다. Mindbody에서 HubSpot 연락처로 동기화되는 판매, 수업 예약, 예약, 멤버십, 계약 정보도 즉시 이루어집니다. Mindbody 예약 파이프라인은 15분마다 업데이트됩니다. 방문 및 Mindbody 판매 파이프라인은 하루에 한 번 업데이트됩니다.",
    "Client auto-creation": "고객 자동 생성",
    "Client profiles and key activities sync instantly. Visits reconcile daily.":
        "고객 프로필과 주요 활동이 즉시 동기화됩니다. 방문은 매일 조정됩니다.",
    "Client profiles, appointments, and sales sync instantly or within minutes.":
        "고객 프로필, 예약, 판매가 즉시 또는 몇 분 이내에 동기화됩니다.",
    "Client service depletion alerts": "고객 서비스 소진 알림",
    "Client syncing from Mindbody → Zoho CRM happens automatically. Zoho CRM → Mindbody sync is triggered by marking leads or contacts to sync manually or via automation.":
        "Mindbody에서 Zoho CRM으로의 고객 동기화는 자동으로 이루어집니다. Zoho CRM에서 Mindbody로의 동기화는 리드나 연락처를 수동 또는 자동화를 통해 동기화 표시하여 트리거됩니다.",
    "Client/profile changes, bookings, visits, sales, services, memberships and contracts post to HighLevel within seconds of appearing in Mindbody. The same applies in reverse when you trigger a push from HighLevel. A nightly reconciliation pass ensures nothing is missed.":
        "고객/프로필 변경, 예약, 방문, 판매, 서비스, 멤버십, 계약이 Mindbody에 나타난 후 몇 초 이내에 HighLevel에 게시됩니다. HighLevel에서 전달을 트리거하면 반대 방향도 동일하게 적용됩니다. 야간 조정으로 누락이 없도록 보장합니다.",
    "Clients are matched by email. If an existing email is found, the Keap profile updates automatically to avoid duplicates.":
        "고객은 이메일로 매칭됩니다. 기존 이메일이 발견되면 중복을 방지하기 위해 Keap 프로필이 자동으로 업데이트됩니다.",
    "Clients are matched in Klaviyo based on their email address - if an existing email is found, the profile is updated; otherwise, a new profile is created. This ensures accurate data without duplicates.":
        "고객은 이메일 주소를 기반으로 Klaviyo에서 매칭됩니다. 기존 이메일이 발견되면 프로필이 업데이트되고, 그렇지 않으면 새 프로필이 생성됩니다. 중복 없이 정확한 데이터를 보장합니다.",
    "Clients book in Mindbody but never get the Zoom link, leading to missed virtual sessions and frustrated customers.":
        "고객이 Mindbody에서 예약하지만 Zoom 링크를 받지 못해, 가상 세션을 놓치고 고객이 불만족하게 됩니다.",
    "Clients can't buy your products or services outside your physical location. Every hour you're closed is revenue walking away.":
        "고객이 물리적 위치 밖에서 제품이나 서비스를 구매할 수 없습니다. 문을 닫는 매 시간이 떠나는 매출입니다.",
    "Clients without an email in Mindbody are not added to Klaviyo.":
        "Mindbody에 이메일이 없는 고객은 Klaviyo에 추가되지 않습니다.",
    "Clients without an email in Mindbody will not be synced to Keap, ensuring data accuracy.":
        "Mindbody에 이메일이 없는 고객은 데이터 정확성을 보장하기 위해 Keap에 동기화되지 않습니다.",
    "Cliniko + ActiveCampaign Integration and Automation | APIANT": "Cliniko + ActiveCampaign 통합 및 자동화 | APIANT",
    "Cliniko + HubSpot Integration and Automation | APIANT": "Cliniko + HubSpot 통합 및 자동화 | APIANT",
    "Cliniko + Salesforce Integration and Automation | APIANT": "Cliniko + Salesforce 통합 및 자동화 | APIANT",
    "Cliniko API Apps": "Cliniko API Apps",
    "Cliniko Appointment Tracking": "Cliniko 예약 추적",
    "Cliniko Appointments Pipeline": "Cliniko 예약 파이프라인",
    "Cliniko Appointments as Salesforce Objects": "Salesforce 오브젝트로서의 Cliniko 예약",
    "Cliniko Integrations": "Cliniko 통합",
    "Cliniko Invoices Pipeline": "Cliniko 인보이스 파이프라인",
    "Cliniko Invoices as Salesforce Objects": "Salesforce 오브젝트로서의 Cliniko 인보이스",
    "Cliniko Invoices in Salesforce": "Salesforce의 Cliniko 인보이스",
    "Cliniko Tech Partner": "Cliniko 기술 파트너",
    "Cliniko Technology Partner": "Cliniko 기술 파트너",
    "Cliniko Turnkey Integration Solutions": "Cliniko 턴키 통합 솔루션",
    "Cliniko and ActiveCampaign": "Cliniko 및 ActiveCampaign",
    "Cliniko and HubSpot": "Cliniko 및 HubSpot",
    "Cliniko and Salesforce": "Cliniko 및 Salesforce",
    "Cliniko is a complete practice management application used by thousands of healthcare practitioners in more than 95 countries worldwide. Manage schedules, treatment notes, invoices, payments and lots more. It works great for solo practitioners, large teams and anything in between.":
        "Cliniko는 전 세계 95개 이상의 국가에서 수천 명의 의료 실무자가 사용하는 완전한 진료 관리 애플리케이션입니다. 일정, 치료 노트, 인보이스, 결제 등을 관리합니다. 개인 실무자, 대규모 팀, 그 사이의 모든 규모에 적합합니다.",
    "Close-up": "클로즈업",
    "Co-Pilot": "Co-Pilot",
    "Code Sync Dropdowns": "Code Sync 드롭다운",
    "Code generation with live API calls": "실시간 API 호출을 통한 코드 생성",
    "Code sent!": "코드가 전송되었습니다!",
    "CodeSync for Dropdowns": "드롭다운용 CodeSync",
    "CodeSync for dropdowns": "드롭다운용 CodeSync",
    "Cody R.": "Cody R.",
    "Combine UI, automation, and AI in one surface for internal operations. Build dashboards, admin panels, and workflow tools that connect to any system in your stack.":
        "내부 운영을 위해 UI, 자동화, AI를 하나의 화면에 결합합니다. 스택의 모든 시스템에 연결되는 대시보드, 관리자 패널, 워크플로우 도구를 구축합니다.",
    "Combine an agent's reasoning with the platform's execution layer: AI that moves data, triggers processes, and resolves issues autonomously.":
        "에이전트의 추론과 플랫폼의 실행 계층을 결합합니다. 데이터를 이동하고, 프로세스를 트리거하고, 문제를 자율적으로 해결하는 AI.",
    "Community": "커뮤니티",
    "Community / generic": "커뮤니티 / 일반",
    "Community forum support": "커뮤니티 포럼 지원",
    "Company": "회사",
    "Company name": "회사명",
    "Company website": "회사 웹사이트",
    "Compare plans": "플랜 비교",
    "Comparison of shallow integration with a single fragile connection versus deep integration with multiple data streams and error handling":
        "단일 취약 연결의 얕은 통합과 여러 데이터 스트림 및 오류 처리의 깊은 통합 비교",
    "Compete with iPaaS Providers": "iPaaS 제공업체와 경쟁",
    "Complete": "완료",
    "Complete Customization & Branding": "완전한 맞춤 설정 및 브랜딩",
    "Complete virtual fitness solution that bridges Mindbody and Zoom. Automated scheduling, attendance tracking, secure meeting links, and client communications enable seamless live-streaming classes at scale.":
        "Mindbody와 Zoom을 연결하는 완전한 가상 피트니스 솔루션. 자동 일정 관리, 출석 추적, 보안 미팅 링크, 고객 커뮤니케이션으로 대규모 라이브 스트리밍 수업을 원활하게 진행합니다.",
    "Complete: your brand, your domain, your UX": "완전: 자체 브랜드, 자체 도메인, 자체 UX",
    "Completed appointment": "완료된 예약",
    "Complex custom engineering": "복잡한 맞춤 엔지니어링",
    "Complex setup": "복잡한 설정",
    "Compliance Monitoring": "컴플라이언스 모니터링",
    "Compliance Ready": "컴플라이언스 준비 완료",
    "Comprehensive Attendance Reports": "종합 출석 보고서",
    "Comprehensive Client Activity Sync": "종합 고객 활동 동기화",
    "Comprehensive Multi-Location Management": "종합 다중 지점 관리",
    "Comprehensive Purchases & Payments": "종합 구매 및 결제",
    "Comprehensive Purchases & Payments Integration": "종합 구매 및 결제 통합",
    "Comprehensive Revenue Visibility": "종합 매출 가시성",
    "Comprehensive Visit & Activity Sync": "종합 방문 및 활동 동기화",
    "Comprehensive Visit and Activity Sync": "종합 방문 및 활동 동기화",
    "Compromised: inadequate safeguards for critical business data": "취약: 중요 비즈니스 데이터에 대한 부적절한 보호",
    "Concrete example:": "구체적인 예시:",
    "Condition(s)": "조건",
    "Conditional Branching": "조건부 분기",
    "Conditional Execution [Data Stream] #4": "조건부 실행 [데이터 스트림] #4",
    "Conditional Logic and Branching": "조건부 로직 및 분기",
    "Conditional branching": "조건부 분기",
    "Conditional branching based on settings": "설정 기반 조건부 분기",
    "Configurable Workflows:": "구성 가능한 워크플로우:",
    "Configuration panel": "구성 패널",
    "Configure": "구성",
    "Configure the number of future days based on how far in advance your appointments are typically booked. A higher value (e.g., 45 days) is ideal if you schedule appointments well in advance. To adjust this setting, contact support@apiant.com.":
        "예약이 일반적으로 얼마나 앞서 이루어지는지에 따라 미래 일수를 구성하세요. 예약을 미리 잡는 경우 더 높은 값(예: 45일)이 적합합니다. 이 설정을 조정하려면 support@apiant.com에 문의하세요.",
    "Configured Once. Enforced Everywhere.": "한 번 구성. 모든 곳에서 적용.",
    "Configures authentication automatically": "인증을 자동으로 구성합니다",
    "Connect": "연결",
    "Connect Mindbody to thousands of apps through Zapier. Webhook-based triggers with enriched data enable powerful automations for client management, appointment bookings, class schedules, sales, and memberships--no coding required.":
        "Zapier를 통해 Mindbody를 수천 개의 앱에 연결하세요. 보강된 데이터가 포함된 webhook 기반 트리거로 고객 관리, 예약, 수업 일정, 판매, 멤버십을 위한 강력한 자동화를 구현합니다. 코딩이 필요 없습니다.",
    "Connect unlimited Zoom accounts to effortlessly run multiple classes at the same time.":
        "무제한 Zoom 계정을 연결하여 여러 수업을 동시에 손쉽게 진행하세요.",
    "Connect with Alex": "Alex와 연결하기",
    "Connected locations": "연결된 지점",
    "Connecting Mindbody to Zapier with AppConnect is a quick and easy, self-guided process. Simply follow the step-by-step installation prompts - no technical skills required. From connecting your Mindbody account to setting up Zapier webhooks and activating automations, everything is clearly explained, making integration fast and hassle-free.":
        "AppConnect로 Mindbody를 Zapier에 연결하는 것은 빠르고 쉬운 자기 안내 프로세스입니다. 단계별 설치 안내를 따르기만 하면 됩니다. 기술 지식이 필요 없습니다. Mindbody 계정 연결부터 Zapier webhook 설정, 자동화 활성화까지 모든 것이 명확하게 설명되어, 통합이 빠르고 번거로움 없이 이루어집니다.",
    "Connection": "연결",
    "Connection Sharing": "연결 공유",
    "Connections": "연결",
    "Connectors": "커넥터",
    "Consultation Tagging": "상담 태그 지정",
    "Consultation tagging": "상담 태그 지정",
    "Contact Sync & Activity Tracking": "연락처 동기화 및 활동 추적",
    "Contact Us": "문의하기",
    "Contact record": "연락처 기록",
    "Continue": "계속",
    "Continuously sync client contract and auto-pay statuses, proactively alerting your team about upcoming renewals or payment issues.":
        "고객 계약 및 자동 결제 상태를 지속적으로 동기화하여, 다가오는 갱신이나 결제 문제에 대해 팀에 사전 알림을 보냅니다.",
    "Continuously sync client contract details and auto-pay statuses directly into Zoho CRM.":
        "고객 계약 세부 정보와 자동 결제 상태를 Zoho CRM에 직접 지속적으로 동기화합니다.",
    "Contract & Auto-Pay Sync": "계약 및 자동 결제 동기화",
    "Contract Management": "계약 관리",
    "Contract Management Sync": "계약 관리 동기화",
    "Contracts & Auto-Pay Management": "계약 및 자동 결제 관리",
    "Contracts > Contact sync": "계약 > 연락처 동기화",
    "Control who can access what across your entire APIANT server. Assign roles, manage permissions, and maintain security across your account network. Each team member sees only what they need to see.":
        "전체 APIANT 서버에서 누가 무엇에 접근할 수 있는지 제어합니다. 역할을 할당하고, 권한을 관리하고, 계정 네트워크 전체에서 보안을 유지합니다. 각 팀 구성원은 필요한 것만 볼 수 있습니다.",
    "Conversational AI": "대화형 AI",
    "Cookie Policy": "쿠키 정책",
    "Corinne K.": "Corinne K.",
    "Cost": "비용",
    "Cost Per Customer": "고객당 비용",
    "Cost at scale": "대규모 비용",
    "Country": "국가",
    "Create the solution using APIANT's Assembly Editor and AI Co-Pilot.":
        "APIANT의 Assembly Editor와 AI Co-Pilot을 사용하여 솔루션을 생성하세요.",
    "Creating test task for validation…": "검증을 위한 테스트 작업 생성 중...",
    "Credentials and connection details": "자격 증명 및 연결 세부 정보",
    "Critical security, dedicated infrastructure, custom SLAs, and hands-on support.":
        "핵심 보안, 전용 인프라, 맞춤 SLA, 실질적인 지원.",
    "Cross-Location Reporting": "지점 간 보고",
    "Cross-Regional Client Tracking": "지역 간 고객 추적",
    "Cross-Regional Client Tracking and Location Tagging": "지역 간 고객 추적 및 지점 태그 지정",
    "Cross-Site Class Capability": "사이트 간 수업 기능",
    "Crowdfunding Tracking": "크라우드펀딩 추적",
    "Current usage": "현재 사용량",
    "Current: v3.6 • Deploying: v3.7": "현재: v3.6 • 배포 중: v3.7",
    "Currently your customers will be charged in Shopify. A \"Shopify\" custom payment method will be added to your Mindbody settings which will be used when posting Shopify sales in Mindbody.":
        "현재 고객은 Shopify에서 결제됩니다. Mindbody 설정에 \"Shopify\" 맞춤 결제 방법이 추가되며, Mindbody에서 Shopify 판매를 기록할 때 사용됩니다.",
    "Currently, the integration syncs up to 15 fields due to Mailchimp's own merge-field limits, ensuring you still have space for additional custom fields if needed.":
        "현재 통합은 Mailchimp 자체의 병합 필드 제한으로 인해 최대 15개 필드를 동기화하며, 필요 시 추가 맞춤 필드를 위한 공간을 확보합니다.",
    "Custom": "맞춤",
    "Custom Dev": "맞춤 개발",
    "Custom Email Branding": "맞춤 이메일 브랜딩",
    "Custom Field Mapping": "맞춤 필드 매핑",
    "Custom Field Selection": "맞춤 필드 선택",
    "Custom Field Sync": "맞춤 필드 동기화",
    "Custom Fields & Objects": "맞춤 필드 및 오브젝트",
    "Custom Fields Support": "맞춤 필드 지원",
    "Custom Fields Sync": "맞춤 필드 동기화",
    "Custom Fields and Objects (Optional)": "맞춤 필드 및 오브젝트 (선택 사항)",
    "Custom Object Mapping": "맞춤 오브젝트 매핑",
    "Custom build": "맞춤 구축",
    "Custom business logic of any complexity": "모든 복잡도의 맞춤 비즈니스 로직",
    "Custom code": "맞춤 코드",
    "Custom fields": "맞춤 필드",
    "Custom fields synced bi-directionally per contact": "연락처당 양방향 동기화되는 맞춤 필드",
    "Custom integration projects end. Products don't. Every customer you add compounds your revenue without proportionally increasing your effort. Build once, collect monthly. Forever.":
        "맞춤 통합 프로젝트는 끝납니다. 제품은 끝나지 않습니다. 추가하는 모든 고객이 노력을 비례적으로 증가시키지 않으면서 매출을 복리로 증가시킵니다. 한 번 구축하고, 매월 수금하세요. 영원히.",
    "Custom object mapping": "맞춤 오브젝트 매핑",
    "Custom object types": "맞춤 오브젝트 유형",
    "Custom objects, computed fields, full entity graphs": "맞춤 오브젝트, 계산 필드, 전체 엔터티 그래프",
    "Custom pricing for your needs.": "요구사항에 맞는 맞춤 가격.",
    "Custom question sync": "맞춤 질문 동기화",
    "Customer Case Study · CRMConnect": "고객 사례 연구 · CRMConnect",
    "Customer Support": "고객 지원",
    "Customer-specific business rules": "고객별 비즈니스 규칙",
    "Customizable Sales Sync Triggers": "맞춤 가능한 판매 동기화 트리거",
    "Customizable business rules and automation paths without requiring technical expertise":
        "기술 전문 지식 없이도 맞춤 가능한 비즈니스 규칙 및 자동화 경로",
    "Customization and Flexibility": "맞춤 설정 및 유연성",
    "Customize exactly when Zoom meetings are created and when emails and SMS notifications are sent, perfectly matching your workflow.":
        "Zoom 미팅 생성 시점과 이메일 및 SMS 알림 전송 시점을 정확히 맞춤 설정하여, 워크플로우에 완벽하게 일치시킵니다.",
    "DEEP INTEGRATION WITH APIANT": "APIANT를 통한 심층 통합",
    "DELETE /tasks/1284 →": "DELETE /tasks/1284 →",
    "DIY Tools (Zapier, Make)": "DIY 도구 (Zapier, Make)",
    "Dashboard": "대시보드",
    "Data Engine": "데이터 엔진",
    "Data Governance": "데이터 거버넌스",
    "Data Nodes - Create Attributes #2": "데이터 노드 - 속성 생성 #2",
    "Data Operations": "데이터 작업",
    "Data Processing Without Compromises": "타협 없는 데이터 처리",
    "Data Rows - Filter": "데이터 행 - 필터",
    "Data Search and Inspection": "데이터 검색 및 검사",
    "Data Search: Client Journey": "데이터 검색: 고객 여정",
    "Data Streams - Split": "데이터 스트림 - 분할",
    "Data Sync & Client Management": "데이터 동기화 및 고객 관리",
    "Data erasure request submitted. Your data will be removed from all systems within 72 hours per our retention policy. You'll receive a confirmation email at jane.doe@example.com when complete.":
        "데이터 삭제 요청이 제출되었습니다. 보존 정책에 따라 72시간 이내에 모든 시스템에서 데이터가 삭제됩니다. 완료되면 jane.doe@example.com으로 확인 이메일을 받으실 수 있습니다.",
    "Data flow between APIs": "API 간 데이터 흐름",
    "Data from all systems is merged, deduplicated, and formatted into a structured report with PDF generation":
        "모든 시스템의 데이터가 병합, 중복 제거되고 PDF 생성과 함께 구조화된 보고서로 포맷됩니다",
    "Data integrity": "데이터 무결성",
    "Data lookups and transformation": "데이터 조회 및 변환",
    "Data lookups from any connected system": "연결된 모든 시스템에서의 데이터 조회",
    "Data processing": "데이터 처리",
    "Data search showing a client ID's full journey through automation":
        "자동화를 통한 고객 ID의 전체 여정을 보여주는 데이터 검색",
    "Data stream": "데이터 스트림",
    "Data synchronization occurs every 15 minutes.": "데이터 동기화는 15분마다 실행됩니다.",
    "Data syncs every 15 minutes.": "데이터가 15분마다 동기화됩니다.",
    "Dave S.": "Dave S.",
    "Days to weeks": "수일에서 수주",
    "Deactivated client (instant)": "비활성화된 고객 (즉시)",
    "Debra S.": "Debra S.",
    "Dedicated APIANT Server": "전용 APIANT 서버",
    "Dedicated AWS Servers (prod + dev)": "전용 AWS 서버 (프로덕션 + 개발)",
    "Dedicated Account Manager": "전담 계정 매니저",
    "Dedicated Infrastructure": "전용 인프라",
    "Dedicated Server Control": "전용 서버 제어",
    "Dedicated account manager": "전담 계정 매니저",
    "Dedicated server: managed by APIANT, owned by you": "전용 서버: APIANT가 관리, 여러분이 소유",
    "Deduplication & Data Mapping": "중복 제거 및 데이터 매핑",
    "Deep (but painfully slow)": "깊은 (그러나 고통스럽게 느린)",
    "Deep Integration Features": "심층 통합 기능",
    "Deep integrations with the platforms that matter": "중요한 플랫폼과의 심층 통합",
    "Deep, but requires specialized developers and months of development":
        "깊지만, 전문 개발자와 수개월의 개발이 필요",
    "Deep: real logic, error handling, custom objects, industry-specific rules":
        "심층: 실제 로직, 오류 처리, 맞춤 오브젝트, 산업별 규칙",
    "Define settings: checkboxes, dropdowns, multi-selects, the controls that shape how each customer consumes the integration.":
        "설정을 정의하세요: 체크박스, 드롭다운, 다중 선택, 각 고객이 통합을 사용하는 방식을 결정하는 컨트롤.",
    "Define what the agent should accomplish and which tools it can use. The agent figures out the steps, executes them, and handles edge cases autonomously.":
        "에이전트가 달성해야 할 목표와 사용할 수 있는 도구를 정의하세요. 에이전트가 단계를 파악하고, 실행하고, 예외 상황을 자율적으로 처리합니다.",
    "Deliver a stunning, seamless online store powered by Shopify - trusted by over a million top global brands - optimized beautifully for desktop and mobile.":
        "전 세계 100만 이상의 최고 브랜드가 신뢰하는 Shopify로 구동되는 멋진 원활한 온라인 스토어를 제공합니다. 데스크톱과 모바일에 아름답게 최적화되어 있습니다.",
    "Deliver seamless virtual classes using Zoom, the global leader known for outstanding video and audio quality, unmatched reliability, and ease of use.":
        "뛰어난 비디오 및 오디오 품질, 비할 데 없는 안정성, 사용 편의성으로 알려진 글로벌 리더 Zoom을 사용하여 원활한 가상 수업을 제공합니다.",
    "Delivers robust, bidirectional integration - with instant Salesforce-to-Cliniko sync and Cliniko-to-Salesforce updates every 15 minutes. Advanced matching and deduplication keep patients, appointments, families, and clinic locations organized, ensuring accurate data, enhanced patient management, and streamlined clinic operations. Trusted globally.":
        "Salesforce에서 Cliniko로의 즉각적인 동기화와 Cliniko에서 Salesforce로의 15분마다 업데이트가 포함된 강력한 양방향 통합을 제공합니다. 고급 매칭 및 중복 제거로 환자, 예약, 가족, 클리닉 지점을 체계적으로 관리하여, 정확한 데이터, 향상된 환자 관리, 간소화된 클리닉 운영을 보장합니다. 전 세계적으로 신뢰받고 있습니다.",
    "Delivery and logging": "전달 및 로깅",
    "Demo & Interactive Example": "데모 및 인터랙티브 예시",
    "Depends on dev": "개발에 따라 다름",
    "Depends on developer implementation": "개발자 구현에 따라 다름",
    "Depends on your implementation": "구현에 따라 다름",
    "Deploy": "배포",
    "Deploy Codebase Group": "코드베이스 그룹 배포",
    "Deploy and Upgrade. All at Once.": "배포하고 업그레이드하세요. 한 번에 모두.",
    "Deploy to All 228 Accounts": "228개 전체 계정에 배포",
    "Deploy to all linked accounts simultaneously. When you push an upgrade, every customer gets it at once -- no manual rollouts, no version drift, no missed locations.":
        "모든 연결된 계정에 동시에 배포합니다. 업그레이드를 전달하면 모든 고객이 한 번에 받습니다. 수동 롤아웃 없음, 버전 차이 없음, 누락된 지점 없음.",
    "Deploy upgrades to all accounts simultaneously": "모든 계정에 동시에 업그레이드 배포",
    "Deployment": "배포",
    "Deployment is atomic. Either all accounts get the update, or none do. Rollback is one click away. You can also deploy to a subset of accounts for staged rollouts before going network-wide.":
        "배포는 원자적입니다. 모든 계정이 업데이트를 받거나, 아무도 받지 않습니다. 롤백은 한 번의 클릭으로 가능합니다. 네트워크 전체 배포 전에 일부 계정에 단계적으로 배포할 수도 있습니다.",
    "Describe your integration need": "통합 요구사항을 설명해 주세요",
    "Detailed Donation Information Sync": "상세 기부 정보 동기화",
    "Detailed Donation Insights": "상세 기부 인사이트",
    "Detailed Email Delivery Reports": "상세 이메일 전달 보고서",
    "DevOps Specialist": "DevOps 전문가",
    "Didn't receive it?": "받지 못하셨나요?",
    "Direct Access to Automation Settings": "자동화 설정에 대한 직접 접근",
    "Directly measure ROI for every advertising campaign within HubSpot. Clearly see which ads, platforms, or assets deliver the highest returns, empowering you to optimize your marketing spend and amplify your most profitable strategies.":
        "HubSpot 내에서 모든 광고 캠페인의 ROI를 직접 측정합니다. 어떤 광고, 플랫폼, 자산이 가장 높은 수익을 제공하는지 명확하게 확인하여, 마케팅 지출을 최적화하고 가장 수익성 높은 전략을 강화할 수 있습니다.",
    "Director of Technology": "기술 이사",
    "Disconnected Care Coordination": "단절된 치료 조율",
    "Disconnected Sales Pipeline": "단절된 판매 파이프라인",
    "Disconnected Tech Stack": "단절된 기술 스택",
    "Disconnected Virtual Experience": "단절된 가상 경험",
    "Discord Community": "Discord 커뮤니티",
    "Discover our other ready-to-use integrations built to simplify your Cliniko workflows and boost your practice's efficiency.":
        "Cliniko 워크플로우를 간소화하고 진료 효율성을 높이는 다른 즉시 사용 가능한 통합을 살펴보세요.",
    "Discover our other ready-to-use integrations built to simplify your DonorPerfect workflows and boost your non-profit's efficiency.":
        "DonorPerfect 워크플로우를 간소화하고 비영리 단체의 효율성을 높이는 다른 즉시 사용 가능한 통합을 살펴보세요.",
    "Discover our other ready-to-use integrations designed to streamline your Mindbody workflows and drive business growth effortlessly.":
        "Mindbody 워크플로우를 간소화하고 비즈니스 성장을 손쉽게 추진하도록 설계된 다른 즉시 사용 가능한 통합을 살펴보세요.",
    "Distribute": "배포",
    "Do I have to create the properties in ActiveCampaign to receive the data from Cliniko?":
        "Cliniko에서 데이터를 받으려면 ActiveCampaign에서 속성을 직접 만들어야 하나요?",
    "Do I have to create the properties in HubSpot to receive the data from Cliniko?":
        "Cliniko에서 데이터를 받으려면 HubSpot에서 속성을 직접 만들어야 하나요?",
    "Do I need technical skills to manage the integration?": "통합을 관리하려면 기술 지식이 필요한가요?",
    "Do I need technical skills to set up AppConnect?": "AppConnect를 설정하려면 기술 지식이 필요한가요?",
    "Do inactive clients count towards my sync limit?": "비활성 고객도 동기화 한도에 포함되나요?",
    "Do you offer nonprofit discounts?": "비영리 단체 할인을 제공하나요?",
    "Do you setup the Salesforce environment as well?": "Salesforce 환경도 설정해 주나요?",
}

# Country names translation
countries = {
    "Afghanistan": "아프가니스탄",
    "Albania": "알바니아",
    "Algeria": "알제리",
    "Andorra": "안도라",
    "Angola": "앙골라",
    "Antigua and Barbuda": "앤티가 바부다",
    "Argentina": "아르헨티나",
    "Armenia": "아르메니아",
    "Australia": "호주",
    "Austria": "오스트리아",
    "Azerbaijan": "아제르바이잔",
    "Bahamas": "바하마",
    "Bahrain": "바레인",
    "Bangladesh": "방글라데시",
    "Barbados": "바베이도스",
    "Belarus": "벨라루스",
    "Belgium": "벨기에",
    "Belize": "벨리즈",
    "Benin": "베냉",
    "Bhutan": "부탄",
    "Bolivia": "볼리비아",
    "Bosnia and Herzegovina": "보스니아 헤르체고비나",
    "Botswana": "보츠와나",
    "Brazil": "브라질",
    "Brunei": "브루나이",
    "Bulgaria": "불가리아",
    "Burkina Faso": "부르키나파소",
    "Burundi": "부룬디",
    "Cambodia": "캄보디아",
    "Cameroon": "카메룬",
    "Canada": "캐나다",
    "Cape Verde": "카보베르데",
    "Central African Republic": "중앙아프리카 공화국",
    "Chad": "차드",
    "Chile": "칠레",
    "China": "중국",
    "Colombia": "콜롬비아",
    "Comoros": "코모로",
    "Congo": "콩고",
    "Costa Rica": "코스타리카",
    "Croatia": "크로아티아",
    "Cuba": "쿠바",
    "Cyprus": "키프로스",
    "Czech Republic": "체코",
    "Denmark": "덴마크",
    "Djibouti": "지부티",
}

ko.update(countries)
translations.update(ko)

# Write the output
with open('/Users/fredericlumiere/apiant-website/i18n/ko_part1.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"Written {len(translations)} translations")
