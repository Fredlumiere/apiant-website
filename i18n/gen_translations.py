#!/usr/bin/env python3
"""Generate all missing KO and JA translations and merge into final files."""
import json

# Load existing
with open('ko.json', 'r') as f:
    ko = json.load(f)
with open('ja.json', 'r') as f:
    ja = json.load(f)

# Load source strings
all_strings = []
for i in range(1, 4):
    with open(f'strings_chunk_{i}.json', 'r') as f:
        all_strings.extend(json.load(f))

missing_ko_list = [s for s in all_strings if s not in ko]
missing_ja_list = [s for s in all_strings if s not in ja]

# Build KO translations dict
ko_trans = {}

# Countries
ko_countries = {"Afghanistan":"아프가니스탄","Albania":"알바니아","Algeria":"알제리","Andorra":"안도라","Angola":"앙골라","Antigua and Barbuda":"앤티가 바부다","Argentina":"아르헨티나","Armenia":"아르메니아","Australia":"호주","Austria":"오스트리아","Azerbaijan":"아제르바이잔","Bahamas":"바하마","Bahrain":"바레인","Bangladesh":"방글라데시","Barbados":"바베이도스","Belarus":"벨라루스","Belgium":"벨기에","Belize":"벨리즈","Benin":"베냉","Bhutan":"부탄","Bolivia":"볼리비아","Bosnia and Herzegovina":"보스니아 헤르체고비나","Botswana":"보츠와나","Brazil":"브라질","Brunei":"브루나이","Bulgaria":"불가리아","Burkina Faso":"부르키나파소","Burundi":"부룬디","Cambodia":"캄보디아","Cameroon":"카메룬","Canada":"캐나다","Cape Verde":"카보베르데","Central African Republic":"중앙아프리카 공화국","Chad":"차드","Chile":"칠레","China":"중국","Colombia":"콜롬비아","Comoros":"코모로","Congo":"콩고","Costa Rica":"코스타리카","Croatia":"크로아티아","Cuba":"쿠바","Cyprus":"키프로스","Czech Republic":"체코","Denmark":"덴마크","Djibouti":"지부티","Moldova":"몰도바","Monaco":"모나코","Mongolia":"몽골","Montenegro":"몬테네그로","Morocco":"모로코","Mozambique":"모잠비크","Myanmar":"미얀마","Namibia":"나미비아","Nauru":"나우루","Nepal":"네팔","Netherlands":"네덜란드","New Zealand":"뉴질랜드","Nicaragua":"니카라과","Niger":"니제르","Nigeria":"나이지리아","Norway":"노르웨이","Oman":"오만","Pakistan":"파키스탄","Palau":"팔라우","Panama":"파나마","Papua New Guinea":"파푸아뉴기니","Paraguay":"파라과이","Peru":"페루","Philippines":"필리핀","Poland":"폴란드","Portugal":"포르투갈"}

ko_trans.update(ko_countries)

# All remaining KO translations
ko_rest = {
"\"1.2s\"":"\"1.2s\"",
"\"501\"":"\"501\"",
"\"A chat is one trigger and one action. Everything between is up to your imagination.\"":"\"채팅은 하나의 트리거와 하나의 액션입니다. 그 사이의 모든 것은 여러분의 상상력에 달려 있습니다.\"",
"\"A chatbot is one trigger and one action. Everything between is up to your imagination.\"":"\"챗봇은 하나의 트리거와 하나의 액션입니다. 그 사이의 모든 것은 여러분의 상상력에 달려 있습니다.\"",
"\"A contact update comes into HubSpot. The master account receives the webhook, identifies which MindBody site the contact belongs to based on the location field, and routes the update to the correct child account. The child account processes it through its own automation with its own MindBody credentials. The contact never knows there are 228 locations behind the scenes.\"":"\"HubSpot에 연락처 업데이트가 들어옵니다. 마스터 계정이 webhook을 수신하고, 위치 필드를 기반으로 해당 연락처가 어느 MindBody 사이트에 속하는지 식별한 후 올바른 자식 계정으로 라우팅합니다. 자식 계정은 자체 MindBody 자격 증명으로 자체 자동화를 통해 처리합니다. 연락처는 배후에 228개 지점이 있다는 사실을 알지 못합니다.\"",
"\"APIANT has proven to be an invaluable asset for our organization. Robust integration solutions.\"":"\"APIANT는 우리 조직에 없어서는 안 될 자산입니다. 견고한 통합 솔루션.\"",
"\"An amazing partner! Has allowed us to develop a comprehensive integration solution.\"":"\"놀라운 파트너! 포괄적인 통합 솔루션 개발을 가능하게 해주었습니다.\"",
"\"Awesomesauce! If you're looking to deliver exceptional results and drive innovation, look no further.\"":"\"최고입니다! 뛰어난 성과와 혁신을 원한다면, 더 찾을 필요 없습니다.\"",
"\"Code Sync\" Dropdowns":"\"Code Sync\" 드롭다운",
"\"CodeSync\" for Dropdowns":"\"CodeSync\" 드롭다운용",
"\"Execute an automation workflow\"":"\"자동화 워크플로우 실행\"",
"\"Fast Theme Changes in Blured have transformed the way I work. Switching between themes on-the-fly helps me align my coding environment with different project requirements swiftly. Glossy has truly streamlined my workflow.\"":"\"Blured의 빠른 테마 변경이 제 작업 방식을 완전히 바꿨습니다. 즉석 테마 전환으로 다양한 프로젝트 요구 사항에 코딩 환경을 빠르게 맞출 수 있습니다. Glossy 덕분에 워크플로우가 크게 간소화되었습니다.\"",
"\"Fast Theme Changes in Blured have transformed the way I work.\"":"\"Blured의 빠른 테마 변경이 제 작업 방식을 완전히 바꿨습니다.\"",
"\"Great Partners! We've been partnering with Apiant since 2019. THANK YOU!\"":"\"훌륭한 파트너! 2019년부터 Apiant와 협력해 왔습니다. 감사합니다!\"",
"\"Great partnership. We are very happy to continue working together with Apiant !\"":"\"훌륭한 파트너십입니다. Apiant와 계속 함께 일할 수 있어 매우 기쁩니다!\"",
"\"List active API connections\"":"\"활성 API 연결 목록 조회\"",
"\"Longtime customer and a huge fan! Absolutely crucial for my biz. Couldn't do it without Apiant.\"":"\"오랜 고객이자 열렬한 팬! 제 사업에 절대적으로 필요합니다. Apiant 없이는 불가능합니다.\"",
"\"Nothing We Have Seen Comes Close To The Power And Versatility Of The APIANT Platform.\"":"\"APIANT 플랫폼의 파워와 다재다능함에 필적하는 것을 본 적이 없습니다.\"",
"\"Powerful Automation, Bespoke Solutions.\"":"\"강력한 자동화, 맞춤형 솔루션.\"",
"\"Professional Team and Excellent Experience. A company that will work with you and for you.\"":"\"프로페셔널한 팀과 탁월한 경험. 고객과 함께, 고객을 위해 일하는 회사.\"",
"\"Query connected system data\"":"\"연결된 시스템 데이터 조회\"",
"\"Real data, real APIs, real business logic. Not sandboxed demos.\"":"\"실제 데이터, 실제 API, 실제 비즈니스 로직. 샌드박스 데모가 아닙니다.\"",
"\"Seamless Implementation and Expert Support! Reliable and effective automation solutions.\"":"\"원활한 구현과 전문가 지원! 신뢰할 수 있고 효과적인 자동화 솔루션.\"",
"\"Seamless Integrations - Professional Service. Has been instrumental in integrating our data factory across more than 200 locations.\"":"\"원활한 통합, 프로페셔널한 서비스. 200개 이상 지점의 데이터 팩토리 통합에 핵심 역할을 했습니다.\"",
"\"The Assembly Editor is where API endpoints become reusable building blocks -- what we call ingredients. Traditionally, this is where builders either accelerate or stall. The ones who master it become unstoppable. The AI Co-Pilot eliminates the learning curve entirely.\"":"\"Assembly Editor는 API 엔드포인트가 재사용 가능한 빌딩 블록(인그리디언트)이 되는 곳입니다. 전통적으로 빌더들이 여기서 가속하거나 멈췄습니다. 마스터한 사람은 막을 수 없게 됩니다. AI Co-Pilot이 학습 곡선을 완전히 제거합니다.\"",
"\"The Deep Integration Gap\"":"\"딥 인테그레이션 갭\"",
"\"The Deep Integration Gap: Bridging the Divide Between Open APIs and Business Needs\"":"\"딥 인테그레이션 갭: 오픈 API와 비즈니스 요구 사이의 격차 해소\"",
"\"The Preeminent Integration & Automation: Everything-You-Could-Ever-Need Platform.\"":"\"최고의 통합 및 자동화: 필요한 모든 것을 갖춘 플랫폼.\"",
"\"The same automation that serves a single-location yoga studio also serves a 228-location franchise. The logic is identical. The settings are different.\"":"\"단일 지점 요가 스튜디오의 자동화가 228개 지점 프랜차이즈에도 동일하게 적용됩니다. 로직은 동일하고, 설정만 다릅니다.\"",
"\"This Is My Bet On Who Wins The API Economy. Incredibly flexible and easy to understand.\"":"\"API 이코노미의 승자는 여기라고 확신합니다. 놀라울 정도로 유연하고 이해하기 쉽습니다.\"",
"\"jane@acme.com\"":"\"jane@acme.com\"",
"\"sync-contact-to-hubspot\"":"\"sync-contact-to-hubspot\"",
}

ko_trans.update(ko_rest)

# Save what we have so far and check count
with open('/tmp/ko_batch_check.json','w') as f:
    json.dump(ko_trans, f, ensure_ascii=False)
print(f"KO translations built: {len(ko_trans)}")
print(f"Still missing: {len(missing_ko_list) - len(ko_trans)}")

# Show first 20 still-missing keys
covered = set(ko_trans.keys())
still_missing = [s for s in missing_ko_list if s not in covered]
for s in still_missing[:20]:
    print(f"  MISSING: {s[:80]}...")
