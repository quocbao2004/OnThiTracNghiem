from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Danh sách câu hỏi và đáp án
questions = [
    {
        'question': 'Mạng máy tính là gì?',
        'options': [
            'Tập hợp những máy tính và thiết bị phần cứng',
            'Kết nối với nhau bằng các kênh truyền thông',
            'Chia sẻ tài nguyên và thông tin với nhau',
            'Tất cả các ý trên'
        ],
        'answer': 'Tất cả các ý trên'
    },
    {
        'question': 'Firewall trong mạng máy tính là gì?',
        'options': [
            'Là thiết bị phần cứng nằm ngoài biên đường mạng',
            'Là thiết bị phần cứng hoặc mềm nằm bên trong đường mạng',
            'Là một hệ thống được thiết kế để ngăn chặn những truy cập không hợp phép',
            'Là hệ thống được thiết kế để dự đoán được truy cập không hợp phép'
        ],
        'answer': 'Là một hệ thống được thiết kế để ngăn chặn những truy cập không hợp phép'
    },
    {
        'question': 'Có bao nhiêu layer trong mô hình OSI?',
        'options': ['4', '5', '6', '7'],
        'answer': '7'
    },
    {
        'question': 'Có bao nhiêu layer trong mô hình TCP/IP?',
        'options': ['4', '5', '6', '7'],
        'answer': '4'
    },
    {
        'question': 'DHCP là chữ viết tắt của:',
        'options': [
            'Dynamic Host Control Protocol',
            'Dynamic Host Configuration Protocol',
            'Dynamic Hyper Control Protocol',
            'Dynamic Hyper Configuration Protocol'
        ],
        'answer': 'Dynamic Host Configuration Protocol'
    },
    {
        'question': 'Ip version 4 có độ dài bao nhiêu bit?',
        'options': ['8', '16', '32', '64'],
        'answer': '32'
    },
    {
        'question': 'DNS là chữ viết tắt của cái gì sau đây?',
        'options': [
            'Dynamic Name System',
            'Dynamic Network System',
            'Domain Name System',
            'Domain Network Service'
        ],
        'answer': 'Domain Name System'
    },
    {
        'question': 'Bandwidth của kênh truyền có nghĩa là?',
        'options': [
            'Kết nối của một máy tính vào mạng local',
            'Khả năng truyền tải của một kênh truyền',
            'Lớp ip được sử dụng trong mạng local',
            'Tất cả đều sai'
        ],
        'answer': 'Khả năng truyền tải của một kênh truyền'
    },
    {
        'question': 'ADSL có nghĩa là gì?',
        'options': [
            'Asymmetric Dual Subscriber Line',
            'Asymmetric Digital System Line',
            'Asymmetric Dual System Line',
            'Asymmetric Digital Subscriber Line'
        ],
        'answer': 'Asymmetric Digital Subscriber Line'
    },
    {
        'question': 'Bridge là thiết bị thường dùng để làm gì trong mạng?',
        'options': [
            'Kết nối những mạng Lan với nhau',
            'Phân chia những mạng Lan với nhau',
            'Tăng tốc độ băng thông với nhau',
            'Cả a,b,c đều đúng'
        ],
        'answer': 'Kết nối những mạng Lan với nhau'
    },
    {
        'question': 'Router là thiết bị làm việc ở tầng mấy trong mô hình OSI?',
        'options': ['6', '5', '4', '3'],
        'answer': '3'
    },
    {
        'question': 'Một gói IP packet chứa thông điệp nào sau đây?',
        'options': [
            'Chỉ có destination address',
            'Chỉ có source address',
            'Một trong hai source hoặc destination address',
            'Cả a,b,c đều sai'
        ],
        'answer': 'Cả a,b,c đều sai'
    },
    {
        'question': 'Bridge là thiết bị hoạt động ở tầng nào trong mô hình OSI?',
        'options': ['2', '3', '4', '7'],
        'answer': '2'
    },
    {
        'question': 'Giao thức nào sau đây cung cấp kết nối đáng tin cậy để gửi những thông điệp?',
        'options': ['TCP', 'UDP', 'IP', 'Cả a,b,c đều đúng'],
        'answer': 'TCP'
    },
    {
        'question': 'Giao thức nào sau đây cung cấp kết nối host to host?',
        'options': ['TCP', 'UDP', 'IP', 'Cả a,b,c đều đúng'],
        'answer': 'TCP'
    },
    {
        'question': 'Class IP nào được sử dụng cho Multicast?',
        'options': ['A', 'B', 'C', 'D'],
        'answer': 'D'
    },
    {
        'question': 'Địa chỉ IP đầu tiên của Class A có 8 bit đầu tiên có dạng như thế nào?',
        'options': ['10000000', '00000001', '11011011', '11110000'],
        'answer': '00000001'
    },
    {
        'question': 'Class IP lớp B có địa chỉ thập phân có dạng như sau:',
        'options': ['128.x.x.x-191.x.x.x', '1.x.x.x-126.x.x.x', '192.x.x.x-223.x.x.x', '240.x.x.x-252.x.x.x'],
        'answer': '128.x.x.x-191.x.x.x'
    },
    {
        'question': 'Class lớp C có địa chỉ IP cuối cùng có 8 bit đầu tiên dạng nhị phân như thế nào?',
        'options': ['10000000', '10111111', '11011111', 'Cả a,b,c đều sai'],
        'answer': '10111111'
    },
    {
        'question': 'Địa chỉ IP đầu tiên của class lớp B có 8 bit đầu tiên có dạng là?',
        'options': ['10000000', '10111111', '10011111', 'Cả a,b,c đều sai'],
        'answer': '10000000'
    },
    {
        'question': 'Địa chỉ cuối cùng của class lớp A có 8 bit đầu tiên có dạng?',
        'options': ['01111111', '00000001', '01000001', 'Cả a,b,c đều sai'],
        'answer': '01111111'
    },
    {
        'question': 'Địa chỉ đầu tiên của IP lớp C có 8 bit đầu tiên có dạng nhị phân?',
        'options': ['11000000', '11100000', '11110000', '11111000'],
        'answer': '11000000'
    },
    {
        'question': 'Địa chỉ IP cuối cùng của lớp C có 8 bit đầu tiên có dạng nhị phân như thế nào?',
        'options': ['11011111', '11101111', '11110111', 'Cả a,b,c đều sai'],
        'answer': '11011111'
    },
    {
        'question': 'Số đường mạng của lớp mạng lớp A là:',
        'options': ['2^7 - 2', '2^14 - 2', '2^21 - 2', '2^8 - 2'],
        'answer': '2^7 - 2'
    },
    {
        'question': 'Số đường mạng của lớp mạng lớp B là:',
        'options': ['2^7 - 2', '2^14 - 2', '2^21 - 2', '2^8 - 2'],
        'answer': '2^14 - 2'
    },
    {
        'question': 'Số đường mạng của lớp mạng lớp C là:',
        'options': ['2^7 - 2', '2^14 - 2', '2^21 - 2', '2^8 - 2'],
        'answer': '2^21 - 2'
    },
    {
        "question": "Địa chỉ network private lớp A là địa chỉ nào sau đây?",
        "options": [
            "10.0.0.0",
            "172.16.0.0",
            "172.31.0.0",
            "192.168.0.0"
        ],
        "answer": "10.0.0.0"
    },
    {
        "question": "Địa chỉ network private lớp B có dạng nào sau đây?",
        "options": [
            "10.0.0.0",
            "172.31.0.0",
            "192.168.0.0",
            "Cả a,b,c đều đúng"
        ],
        "answer": "172.31.0.0"
    },
    {
        "question": "Địa chỉ chỉ network private lớp C có dạng nào sau đây?",
        "options": [
            "10.0.0.0",
            "172.16.0.0",
            "172.31.0.0",
            "192.168.0.0"
        ],
        "answer": "192.168.0.0"
    },
    {
        "question": "Subnet mask nào sau đây là của địa chỉ network private lớp A?",
        "options": [
            "255.0.0.0",
            "255.240.0.0",
            "255.255.240.0",
            "255.255.255.240"
        ],
        "answer": "255.0.0.0"
    },
    {
        "question": "Subnet mask nào sau đây là của địa chỉ network private lớp B?",
        "options": [
            "255.0.0.0",
            "255.240.0.0",
            "255.255.240.0",
            "255.255.255.240"
        ],
        "answer": "255.240.0.0"
    },
    {
        "question": "Subnet mask nào sau đây là của địa chỉ network private lớp C?",
        "options": [
            "255.0.0.0",
            "255.240.0.0",
            "255.255.240.0",
            "255.255.255.0"
        ],
        "answer": "255.255.255.0"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về đường mạng lớp B?",
        "options": [
            "Network 14 bit host bit 16",
            "Network 16 bit host bit 16",
            "Network 18 bit và host 14",
            "Network 16 bit và host 14 bit"
        ],
        "answer": "Network 16 bit host bit 16"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về đường mạng lớp A?",
        "options": [
            "Network 7 bit host bit 24 bit",
            "Network 8 bit host bit 24",
            "Network 16 bit và host 16",
            "Network 15 bit và host 16 bit"
        ],
        "answer": "Network 8 bit host bit 24"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về đường mạng lớp C?",
        "options": [
            "Network 21 bit host bit 8",
            "Network 24 bit host bit 8",
            "Network 16 bit và host 14",
            "Network 18 bit và host 14 bit"
        ],
        "answer": "Network 24 bit host bit 8"
    },
{
        "question": "Lớp địa chỉ IP nào sau đây được sử dụng cho multicast?",
        "options": [
            "A",
            "B",
            "C",
            "D"
        ],
        "answer": "D"
    },
    {
        "question": "Địa chỉ IP cuối cùng trong một đường mạng thể hiện điều gì?",
        "options": [
            "Địa chỉ IP",
            "Địa chỉ net",
            "Địa chỉ host",
            "Địa chỉ broadcast"
        ],
        "answer": "Địa chỉ broadcast"
    },
    {
        "question": "Layer nào sau đây được gọi là end to end layer?",
        "options": [
            "Presentation",
            "Application",
            "Transport",
            "Network"
        ],
        "answer": "Transport"
    },
    {
        "question": "Tại sao giao thức IP được gọi là giao thức không tin cậy?",
        "options": [
            "Mất mát gói tin",
            "Trùng lặp gói tin",
            "Trễ gói tin",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Cả a,b,c đều đúng"
    },
    {
        "question": "Minimum header size trong gói IP có độ dài bao nhiêu byte?",
        "options": [
            "10",
            "16",
            "20",
            "24"
        ],
        "answer": "20"
    },
    {
        "question": "Địa chỉ IP version 6 có bao nhiêu bit?",
        "options": [
            "32",
            "64",
            "96",
            "128"
        ],
        "answer": "128"
    },
    {
        "question": "Router làm điều gì sau đây trong mạng khi nhận được một gói tin?",
        "options": [
            "Forwarding gói tin đến tất cả đường link",
            "Forwarding gói tin đến đường link rảnh rỗi",
            "Forwarding gói tin đến đường link được xác định trong routing table",
            "Forwarding gói tin đến tất cả đường link ngoài trừ đường link gởi"
        ],
        "answer": "Forwarding gói tin đến đường link được xác định trong routing table"
    },
    {
        "question": "Cái nào sau đây có thể có phần mềm?",
        "options": [
            "Router",
            "Firewall",
            "Gateway",
            "Modems"
        ],
        "answer": "Firewall"
    },
    {
        "question": "Sử dụng lệnh Ping để làm điều nào sau đây?",
        "options": [
            "Kiểm tra ổ đĩa",
            "Kiểm tra thiết bị phần cứng",
            "Kiểm tra thiết bị mạng có thể truy cập được",
            "Cả a,b,c đều sai"
        ],
        "answer": "Kiểm tra thiết bị mạng có thể truy cập được"
    },
    {
        "question": "MAC address là địa chỉ được sử dụng trong tầng nào?",
        "options": [
            "Application",
            "Transport",
            "Network",
            "Data Link"
        ],
        "answer": "Data Link"
    },
    {
        "question": "Routing table có nhiệm vụ gì sau đây là đúng?",
        "options": [
            "Gán địa chỉ MAC Address",
            "Phân bố địa chỉ IP đến các port",
            "Sử dụng để forward packet đến các destination",
            "Chuyển địa chỉ MAC thành địa chỉ IP"
        ],
        "answer": "Sử dụng để forward packet đến các destination"
    },
    {
        "question": "Cái nào sau đây là đúng khi nói về Broadcast?",
        "options": [
            "Gửi gói tin đến tất cả các máy",
            "Gửi gói tin đến một số máy",
            "Gửi gói tin đến một số máy trừ một máy",
            "Gửi gói tin đến một số máy trừ một vài máy tính"
        ],
        "answer": "Gửi gói tin đến tất cả các máy"
    },
    {
        "question": "Đâu là giao thức nằm ở tầng Application?",
        "options": [
            "FTP",
            "TCP",
            "A và b đều đúng",
            "A và b đều sai"
        ],
        "answer": "FTP"
    },
    {
        "question": "Đâu là dãy địa chỉ IP được gọi là APIPA?",
        "options": [
            "169.254.0.1 to 169.254.0.254",
            "169.254.0.1 to 169.254.0.255",
            "169.254.0.1 to 169.254.255.254",
            "169.254.0.1 to 169.254.255.255"
        ],
        "answer": "169.254.0.1 to 169.254.255.255"
    },
    {
        "question": "Số byte của địa chỉ IP trong IP header có độ dài bao nhiêu?",
        "options": [
            "4",
            "8",
            "16",
            "32"
        ],
        "answer": "4"
    },
    {
        "question": "Trong TCP header PSH flag thường được sử dụng khi nào?",
        "options": [
            "Kết thúc một message",
            "Khởi đầu một tin nhắn",
            "Push một message",
            "Dừng một message"
        ],
        "answer": "Push một message"
    },
    {
        "question": "Đâu là subnet mask cho dãy địa chỉ lớp C?",
        "options": [
            "255.255.25.0",
            "255.255.255.0",
            "255.0.0.255",
            "255.0.255.255"
        ],
        "answer": "255.255.255.0"
    },
    {
        "question": "2 device được gọi là trong mạng nếu?",
        "options": [
            "Một process trên device này có trao đổi thông tin với một tiến trình trên device còn lại",
            "Hai device đều sử dụng chung một tiến trình mạng",
            "Hai device chạy chung một application",
            "A,b,c đều sai"
        ],
        "answer": "Một process trên device này có trao đổi thông tin với một tiến trình trên device còn lại"
    },
    {
        "question": "Nhiều đối tượng được gửi qua TCP được gọi là?",
        "options": [
            "Persistent",
            "Nonpersistent",
            "A và b đều đúng",
            "A và b đều sai"
        ],
        "answer": "Persistent"
    },
    {
        "question": "HTTP là một giao thức nằm ở tầng nào trong mô hình OSI?",
        "options": [
            "Application",
            "Network",
            "Datalink",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Application"
    },
        {
        "question": "Giao thức nào tầng transport được sử dụng cho giao thức HTTP?",
        "options": ["UDP", "TCP", "IP", "ATM"],
        "answer": "TCP"
    },
    {
        "question": "Trong HTTP pipeline thì cái gì sau đây là đúng?",
        "options": [
            "Nhiều HTTP request được gởi trên một kết nối TCP mà không cần đợi response",
            "Nhiều HTTP request được gởi trên nhiều kết nối TCP mà không cần đợi response",
            "Nhiều HTTP được lưu trữ trong một queue rồi gởi theo cơ chế FIFO",
            "Cả a,b,c đều sai"
        ],
        "answer": "Nhiều HTTP request được gởi trên một kết nối TCP mà không cần đợi response"
    },
    {
        "question": "FTP listen connection ở số port bao nhiêu?",
        "options": ["20", "21", "22", "19"],
        "answer": "21"
    },
    {
        "question": "FTP truyền tải thông tin thông qua kết nối TCP port bao nhiêu?",
        "options": ["20", "21", "22", "19"],
        "answer": "20"
    },
    {
        "question": "Trong giao thức FTP client và server sử dụng giao thức nào sau đây để truyền tải thông tin?",
        "options": ["TCP", "UDP", "Cả a và b đều đúng", "Cả a và b đều sai"],
        "answer": "TCP"
    },
    {
        "question": "Trong giao thức FTP, client đều chủ động tạo kết nối cả control và data connection được là FTP Mode nào?",
        "options": ["Active", "Passive", "Hybrid", "Cả a,b,c đều sai"],
        "answer": "Passive"
    },
    {
        "question": "Giao thức FTP được xây dựng theo mô hình nào?",
        "options": ["Data center", "Phân tán", "Client server", "Rời rạc"],
        "answer": "Client server"
    },
    {
        "question": "Ethernet Frame header có thông tin nào sau đây?",
        "options": ["IP address", "MAC address", "Cả a và b", "Không có a và b"],
        "answer": "MAC address"
    },
    {
        "question": "MAC address là một thông tin gồm bao nhiêu bit?",
        "options": ["32", "40", "48", "64"],
        "answer": "48"
    },
    {
        "question": "Giao thức kết nối point-to-point (PPP) là giao thức:",
        "options": [
            "Đóng gói PPP frame bên trong Ethernet frame",
            "Đóng gói Ethernet frame bên trong PPP frame",
            "Cả a và b",
            "Cả a và b đều sai"
        ],
        "answer": "Đóng gói Ethernet frame bên trong PPP frame"
    },
    {
        "question": "Maximum size của dữ liệu của Ethernet frame có giá trị bằng bao nhiêu?",
        "options": ["1000", "1200", "1300", "1500"],
        "answer": "1500"
    },
    {
        "question": "Loại topology nào mà trung tâm là một hub hoặc switch?",
        "options": ["Ring", "Star", "Mesh", "Bus"],
        "answer": "Star"
    },
    {
        "question": "Loại topology network nào sau đây có sự mở rộng dễ nhất, đơn giản nhất?",
        "options": ["Star", "Ring", "Bus", "Cả a,b,c đều như nhau"],
        "answer": "Star"
    },
    {
        "question": "Truyền thông kết nối giữa các quốc gia, các châu lục trên thế giới được gọi là?",
        "options": ["LAN", "WAN", "MAN", "Cả a,b,c đều sai"],
        "answer": "WAN"
    },
    {
        "question": "Nếu có N router từ A đến B, với mỗi packet có số Bit là L, và R là tốc độ truyền thì thời gian delay từ A đến B là bao nhiêu?",
        "options": ["N", "(N*L)/R", "2(N*L)/R", "Cả a,b,c đều sai"],
        "answer": "(N*L)/R"
    },
    {
        "question": "Resource cần thiết để truyền thông giữa 2 thiết bị đầu cuối được dành riêng trong suốt thời gian session làm việc là?",
        "options": ["Chuyển mạch gói", "Chuyển mạch mạch", "Cả a và b", "Cả a và b đều sai"],
        "answer": "Chuyển mạch mạch"
    },
    {
        "question": "Giao thức IP không làm được điều gì sau đây?",
        "options": [
            "Định nghĩa địa chỉ ip",
            "Cung cấp dịch vụ cho tầng transport",
            "Hỗ trợ báo cáo lỗi",
            "Định nghĩa ip packet"
        ],
        "answer": "Hỗ trợ báo cáo lỗi"
    },
    {
        "question": "Trong IPv4 thì trường nào sau đây không liên quan đến IP fragment?",
        "options": ["FLAGS", "OFFSET", "TOS", "Identifier"],
        "answer": "TOS"
    },
    {
        "question": "Packet có TTL = 10, vậy số router Max mà packet này có thể đi qua là?",
        "options": ["9", "10", "11", "12"],
        "answer": "10"
    },
    {
        "question": "Trong IP header với protocol field = 17 thì giao thức tầng transport là gì?",
        "options": ["TCP", "UDP", "ICMP", "Cả a,b,c đều sai"],
        "answer": "UDP"
    },
    {
        "question": "Với gói packet fragment cuối cùng thì flag có giá trị là?",
        "options": ["0", "1", "10", "01"],
        "answer": "0"
    },
    {
        "question": "IP protocol không cung cấp dịch vụ nào sau đây?",
        "options": [
            "Truyền thông phi kết nối",
            "Truyền thông đáng tin cậy",
            "Cả a,b,c đều đúng",
            "Cả a,b,c đều sai"
        ],
        "answer": "Truyền thông đáng tin cậy"
    },
    {
        "question": "IP fragment là cách thức có hạn chế nào sau đây?",
        "options": [
            "Định tuyến phức tạp",
            "Có thể gây DDOS",
            "Có thể trùng fragment",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Cả a,b,c đều đúng"
    },
    {
        "question": "Đâu là trường được sử dụng trong quá trình refragment?",
        "options": ["Offset", "Flag", "TTL", "Identifier"],
        "answer": "Offset"
    },
    {
        "question": "Độ dài lớn của datagram header IP version 6 có độ dài bao nhiêu?",
        "options": ["10 bytes", "20 bytes", "30 bytes", "40 bytes"],
        "answer": "40 bytes"
    },
    {
        "question": "Trong IP header của IP version 6 thì trường nào sau đây giữ nguyên so với IP version 4?",
        "options": ["Fragment field", "Offset", "TOS", "Cả a,b,c đều giữ nguyên"],
        "answer": "TOS"
    },
    {
        "question": "DHCP là dịch vụ cung cấp điều gì sau đây?",
        "options": ["MAC address", "IP address", "Cả a,b đều đúng", "Cả a,b đều sai"],
        "answer": "IP address"
    },
    {
        "question": "DHCP được sử dụng cho?",
        "options": ["IP version 6", "IP version 4", "Cả a,b đều đúng", "Cả a,b đều sai"],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "DHCP client gởi dữ liệu đến DHCP server thông qua UDP port bao nhiêu?",
        "options": ["66", "67", "68", "69"],
        "answer": "68"
    },
    {
        "question": "DHCP server có thể cung cấp địa chỉ IP?",
        "options": ["Static", "Dynamic", "Automatic", "Cả a,b,c đều đúng"],
        "answer": "Cả a,b,c đều đúng"
    },
    {
        "question": "DHCP client và server trong một subnet sử dụng cái nào sau đây để giao tiếp?",
        "options": ["UDP broadcast", "UDP unicast", "TCP broadcast", "TCP unicast"],
        "answer": "UDP broadcast"
    },
    {
        "question": "Sau khi nhận địa chỉ IP thì client sử dụng giao thức nào để xác định trùng lặp địa chỉ IP?",
        "options": [
            "Internet relay chat",
            "Address resolution protocol",
            "Border gateway protocol",
            "Cả a,b,c đều sai"
        ],
        "answer": "Address resolution protocol"
    },
    {
        "question": "DHCP snooping là gì?",
        "options": [
            "Thuật toán phân bố DHCP",
            "Mã hóa DHCP request",
            "Là một kỹ thuật được sử dụng nâng cao bảo mật của DHCP",
            "Cả a,b,c đều sai"
        ],
        "answer": "Là một kỹ thuật được sử dụng nâng cao bảo mật của DHCP"
    },
    {
        "question": "Ở Network layer thì data được gọi là?",
        "options": ["Frame", "Packet", "Datagram", "Cả a,b,c đều sai"],
        "answer": "Packet"
    },
    {
        "question": "ICMP protocol là giao thức để xử lý?",
        "options": [
            "Lỗi và chuẩn đoán",
            "Addressing",
            "Forwarding",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Lỗi và chuẩn đoán"
    },
    {
        "question": "Transport layer tổng hợp message của các Application và chuyển thành các luồng dữ liệu và chuyển xuống?",
        "options": ["Network layer", "Data link layer", "Physical layer", "Cả a,b,c đều sai"],
        "answer": "Network layer"
    },
    {
        "question": "Các giao thức nào sau đây được sử dụng tại Internet?",
        "options": ["TCP", "UDP", "Cả a,b đều đúng", "Cả a,b đều sai"],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "Giá trị nào sau đây không thuộc về tầng Network?",
        "options": ["IP source", "Port des", "TOS", "Cả a,b,c đều đúng"],
        "answer": "Port des"
    },
    {
        "question": "Giao thức tầng Transport layer là giao thức?",
        "options": [
            "Truyền thông kết nối application với application",
            "Truyền thông kết nối process với process",
            "Truyền thông kết nối host với host",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Truyền thông kết nối process với process"
    },
    {
        "question": "Giao thức nào phân giải internet domain name và host name sang địa chỉ IP?",
        "options": [
            "Domain name system",
            "Internet control message system",
            "Dynamic system name control",
            "Cả a,b,c đều sai"
        ],
        "answer": "Domain name system"
    },
    {
        "question": "Giao thức nào sau đây cho phép máy tính điều khiển một máy tính khác từ xa?",
        "options": ["Telnet", "TFTP", "FTP", "Cả a,b,c đều sai"],
        "answer": "Telnet"
    },
    {
        "question": "Application layer protocol làm điều gì sau đây?",
        "options": [
            "Định dạng loại message được trao đổi",
            "Định dạng message, cấu trúc và ngữ pháp message",
            "Định dạng quy tắc luật lệ cho quy trình gởi và nhận message",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Cả a,b,c đều đúng"
    },
    {
        "question": "Đâu là giao thức tầng application giúp gởi lưu trữ mail trên server?",
        "options": [
            "Simple Mail Transfer Protocol",
            "Pop3",
            "Cả a,b đều đúng",
            "Cả a,b đều sai"
        ],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "Đâu là giao thức tầng application giúp client lấy mail?",
        "options": [
            "Simple Mail Transfer Protocol",
            "Pop3",
            "Cả a,b đều đúng",
            "Cả a,b đều sai"
        ],
        "answer": "Pop3"
    },
    {
        "question": "ASCII dùng để encode binary data được gọi là?",
        "options": [
            "Base 64",
            "Base 32",
            "Base 16",
            "Base 8"
        ],
        "answer": "Base 64"
    },
    {
        "question": "Khi hiển thị website thì application layer sử dụng giao thức nào sau đây?",
        "options": [
            "HTTP",
            "FTP",
            "SMTP",
            "Cả a,b,c đều đúng"
        ],
        "answer": "HTTP"
    },
    {
        "question": "Đâu là giao thức không thuộc ở tầng application layer?",
        "options": [
            "SMTP",
            "FTP",
            "TELNET",
            "ICMP"
        ],
        "answer": "ICMP"
    },
    {
        "question": "Data ở tầng application layer được gọi là?",
        "options": ["Datagram", "Packet", "Message", "Cả a,b,c đều sai"],
        "answer": "Message"
    },
    {
        "question": "Đâu là một trong những mô hình kiến trúc?",
        "options": [
            "Client to server",
            "Peer to peer",
            "Cả a,b đều đúng",
            "Cả a,b đều sai"
        ],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "Application layer cung cấp dịch vụ truyền thông dạng?",
        "options": [
            "End to end",
            "Client to end",
            "Client to server",
            "Cả a,b,c đều đúng"
        ],
        "answer": "End to end"
    },
    {
        "question": "Trong truyền thông tại tầng application để gửi chính xác các message đến đúng chương trình trên máy tính thì địa chỉ nào sau đây phải đúng?",
        "options": [
            "IP address",
            "MAC address",
            "Port",
            "Cả a,b,c đều sai"
        ],
        "answer": "Port"
    },
    {
        "question": "Dịch vụ nào sau đây yêu cầu thời gian thực?",
        "options": ["FTP", "TELNET", "TELEPHONE", "MAIL"],
        "answer": "TELEPHONE"
    },
    {
        "question": "Số object của HTTP khi có 4 file JPG và HTML text là?",
        "options": ["4", "5", "1", "3"],
        "answer": "5"
    },
    {
        "question": "Loại kết nối mặc định của HTTP là?",
        "options": [
            "Persistent",
            "Non-persistent",
            "Cả a và b đúng",
            "Cả a và b sai"
        ],
        "answer": "Non-persistent"
    },
    {
        "question": "Khoảng thời gian mà client gửi một packet đến server và phản hồi được gọi là?",
        "options": ["TTL", "RTT", "PTT", "Cả a,b,c đều sai"],
        "answer": "RTT"
    },
    {
        "question": "Khi request HTTP không tìm thấy đường đối tượng thì status code nào sau đây được trả về?",
        "options": ["304", "404", "200", "204"],
        "answer": "404"
    },
    {
        "question": "Điều nào sau đây là không đúng khi nói về web cache?",
        "options": [
            "Web cache không có không gian nhớ riêng",
            "Web cache hoạt động theo mô hình client-server",
            "Web cache có thể giảm thời gian phản hồi",
            "Web cache chứa đối tượng sao chép gần nhất"
        ],
        "answer": "Web cache không có không gian nhớ riêng"
    },
    {
        "question": "Ping trong giao thức ICMP có thể?",
        "options": [
            "Tính RTT",
            "Thống kê mất mát gói tin",
            "Liệt kê độ trễ",
            "Cả a,b,c đều đúng"
        ],
        "answer": "Cả a,b,c đều đúng"
    },
    {
        "question": "ICMP thường sử dụng giao thức con nào sau đây?",
        "options": ["Ping", "Traceroute", "Cả a,b đều đúng", "Cả a,b đều sai"],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "Câu lệnh nào sau đây thường sử dụng để hiện thị bảng định tuyến trong Windows?",
        "options": [
            "Route",
            "Ipconfig",
            "Traceroute",
            "Cả a,b,c đều sai"
        ],
        "answer": "Route"
    },
    {
        "question": "Nếu muốn tìm từ nơi bắt đầu đến kết thúc của packet qua bao nhiêu router thì ta sử dụng câu lệnh nào sau đây?",
        "options": [
            "Ping",
            "Traceroute",
            "Ipconfig",
            "Cả a,b,c đều sai"
        ],
        "answer": "Traceroute"
    },
    {
        "question": "FTP là chữ viết tắt của?",
        "options": [
            "First transfer protocol",
            "File transfer protocol",
            "Fine transfer protocol",
            "Cả a,b,c đều sai"
        ],
        "answer": "File transfer protocol"
    },
    {
        "question": "FTP được xây dựng trên mô hình?",
        "options": [
            "P2p",
            "Client to server",
            "Hybrid",
            "Cả a,b,c đều sai"
        ],
        "answer": "Client to server"
    },
    {
        "question": "Giao thức FTP sử dụng mấy kết nối?",
        "options": ["1", "2", "3", "4"],
        "answer": "2"
    },
    {
        "question": "Client FTP download 5 file từ server FTP số kết nối cần thiết để nhận 5 file là?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "question": "Sử dụng dịch vụ FTP thì password được gửi để xác thực đến server thông qua lệnh nào?",
        "options": [
            "PASSWRD",
            "PASS",
            "PASSWORD",
            "Cả a,b,c đều sai"
        ],
        "answer": "PASS"
    },
    {
        "question": "Loại tấn công DDOS nào mà hacker sử dụng tạo một số lượng lớn kết nối đến server được gọi là?",
        "options": [
            "Bandwidth flooding",
            "Connection flooding",
            "Connection poisoning",
            "Cả a,b,c đều sai"
        ],
        "answer": "Connection flooding"
    },
    {
        "question": "Loại tấn công DOS mà hacker tạo một số lượng lớn truy vấn đến máy chủ mục tiêu được gọi là?",
        "options": [
            "Bandwidth flooding",
            "Connection flooding",
            "Connection poisoning",
            "Cả a,b,c đều sai"
        ],
        "answer": "Bandwidth flooding"
    },
    {
        "question": "Packet sniffer là dạng tấn công?",
        "options": ["Active", "Passive", "Cả a và b đúng", "Cả a,b sai"],
        "answer": "Passive"
    },
    {
        "question": "Sniffer có thể được sử dụng trong?",
        "options": ["Wireless", "Ethernet Lan", "Cả a,b đều đúng", "Cả a,b đều sai"],
        "answer": "Cả a,b đều đúng"
    },
    {
        "question": "Trong header của UDP, trường length là độ dài của thành phần nào sau đây?",
        "options": [
            "Cả segment UDP",
            "Chỉ phần đầu header của UDP",
            "Chỉ phần dữ liệu (payload)",
            "Trong header của UDP không có trường length"
        ],
        "answer": "Cả segment UDP"
    },
    {
        "question": "Trong giao thức TCP, Initial Sequence Number (ISN) sẽ bằng?",
        "options": ["1", "100", "0", "Do hệ điều hành tạo ra bằng 1 thuật toán"],
        "answer": "Do hệ điều hành tạo ra bằng 1 thuật toán"
    },
    {
        "question": "Trường receive window trong header của giao thức TCP sẽ giúp TCP thực hiện việc gì sau đây?",
        "options": [
            "Điều khiển tắc nghẽn",
            "Điều khiển luồng",
            "Quản lý kết nối",
            "Câu A và B đều đúng"
        ],
        "answer": "Điều khiển luồng"
    },
    {
        "question": "Trong TCP slow start, Initial Congestion Window sẽ bằng bao nhiêu MSS?",
        "options": ["1", "2", "Số ngẫu nhiên", "Bằng đúng giá trị ngưỡng (threshold)"],
        "answer": "1"
    },
    {
        "question": "Trong TCP Tahoe, khi gặp trường hợp timeout, thì giá trị của congestion window sẽ được thiết lập lại bao nhiêu?",
        "options": ["1", "Bị cắt một nửa", "0", "Vẫn giữ giá trị như trước khi gặp 3 ACK trùng nhau, và sau đó sẽ tăng theo tuyến tính"],
        "answer": "1"
    },
    {
        "question": "Đặc điểm của kiến trúc P2P thuần túy là gì?",
        "options": [
            "Không có server luôn hoạt động",
            "Liên lạc trực tiếp giữa các hệ thống đầu cuối bất kỳ",
            "Các thiết bị kết nối không liên tục và thay đổi địa chỉ IP",
            "A, B, C đều đúng"
        ],
        "answer": "A, B, C đều đúng"
    },
    {
        "question": "Kích thước phần thông tin tiêu đề (header) của TCP là?",
        "options": ["20 bytes", "4 bytes", "8 bytes", "16 bytes"],
        "answer": "20 bytes"
    },
    {
        "question": "Để cấp phát động địa chỉ IP, ta có thể sử dụng dịch vụ có giao thức nào?",
        "options": ["DHCP", "FTP", "DNS", "HTTP"],
        "answer": "DHCP"
    },
    {
        "question": "Khi dữ liệu được đóng gói (encapsulation), thứ tự nào sau đây là đúng?",
        "options": [
            "Data, frame, packet, segment, bit",
            "Segment, data, packet, frame, bit",
            "Data, segment, packet, frame, bit",
            "Data, segment, frame, packet, bit"
        ],
        "answer": "Data, segment, packet, frame, bit"
    },
    {
        "question": "TCP không cung cấp dịch vụ nào sau đây?",
        "options": [
            "Điều khiển luồng (flow control)",
            "Mã hóa",
            "Điều khiển tắt nghẽn (congestion control)",
            "Hướng kết nối (connection oriented)"
        ],
        "answer": "Mã hóa"
    },
    {
        "question": "Giao thức nào sau đây không làm việc theo cơ chế “nỗ lực tốt nhất” (best-effort)?",
        "options": ["IP", "TCP", "UDP", "Các câu A, B và C đều đúng"],
        "answer": "TCP"
    },
    {
        "question": "Trong RDT 2.0, chuyện gì sẽ xảy ra nếu có phát sinh lỗi trong quá trình truyền dữ liệu?",
        "options": [
            "Bên nhận gửi ACK trùng lặp cho bên gửi để báo hiệu về lỗi phát sinh",
            "Bên gửi phát hiện lỗi sau khi thời gian chờ hết hạn",
            "Bên nhận gửi NAK cho bên gửi để báo hiệu về lỗi phát sinh",
            "Tất cả các câu trả lời đều sai"
        ],
        "answer": "Bên nhận gửi NAK cho bên gửi để báo hiệu về lỗi phát sinh"
    },
    {
        "question": "Trong gói tin TCP yêu cầu kết nối, trường flag sẽ có giá trị của các cờ là gì?",
        "options": [
            "ACK=1, SYN=1, FIN=1",
            "ACK=1, SYN=0, FIN=1",
            "ACK=1, SYN=0, FIN=0",
            "ACK=0, SYN=1, FIN=0"
        ],
        "answer": "ACK=0, SYN=1, FIN=0"
    },
    {
        "question": "Một IP Datagram có kích thước là 2000 bytes. Giả sử IP header và TCP header trong IP Datagram này có chiều dài mặc định. Hãy cho biết kích thước TCP payload của IP Datagram này là bao nhiêu bytes?",
        "options": ["1040 bytes", "1960 bytes", "2040 bytes", "2960 bytes"],
        "answer": "1960 bytes"
    },
    {
        "question": "Khi đóng kết nối TCP, bên gửi và nhận sẽ làm gì?",
        "options": [
            "Chờ time-out và tự động đóng kết nối",
            "Gửi TCP segment với FIN bit = 1",
            "Gửi TCP segment với FIN bit = 0",
            "A, B, C đều sai"
        ],
        "answer": "Gửi TCP segment với FIN bit = 1"
    },
    {
        "question": "Phát biểu nào sau đây là đúng về giao thức FTP?",
        "options": [
            "FTP sử dụng cổng 20 để tạo kết nối điều khiển và cổng 21 để tạo kết nối dữ liệu",
            "FTP sử dụng cổng 21 để tạo kết nối điều khiển và cổng 20 để tạo kết nối dữ liệu",
            "FTP sử dụng cổng 21 để tạo kết nối điều khiển và cổng 22 để tạo kết nối dữ liệu",
            "FTP sử dụng cổng 22 để tạo kết nối điều khiển và cổng 21 để tạo kết nối dữ liệu"
        ],
        "answer": "FTP sử dụng cổng 21 để tạo kết nối điều khiển và cổng 20 để tạo kết nối dữ liệu"
    },
    {
        "question": "Hãy cho biết giá trị UDP Checksum của dữ liệu như sau là bao nhiêu? 1001010010110100 0110101110010010",
        "options": [
            "10000000001000110",
            "01111111110111001",
            "0000000001000111",
            "1111111110111000"
        ],
        "answer": "01111111110111001"
    },
    {
        "question": "Trong quá trình bắt tay 3 bước của một khởi tạo kết nối TCP, nếu Sequence Number của gói SYN là 2000, thì Acknowlegmnet Number của gói SYN/ACK là bao nhiêu?",
        "options": ["2000", "2001", "2002", "Tùy thuộc vào kích thước dữ liệu mà gói TCP này đang mang theo"],
        "answer": "2001"
    },
    {
        "question": "10Mbps thì bằng bao nhiêu Kbps?",
        "options": ["10.000 Kbps", "10.240 Kbps", "80.000 Kbps", "Các câu trên đều sai"],
        "answer": "10.000 Kbps"
    },
    {
        "question": "Nguyên lý truyền tin cậy Rdt 2.1 có cải tiến gì so với Rdt 2.2?",
        "options": [
            "Thêm vào timeout cho mỗi gói tin",
            "Thêm vào 2 số thứ tự (0,1) cho gói tin",
            "Thay cho NAK, bên nhận gửi ACK với số thứ tự là gói cuối cùng được nhận thành công",
            "Cho phép truyền nhiều gói tin một lúc mà không cần đợi báo nhận ACK"
        ],
        "answer": "Thêm vào timeout cho mỗi gói tin"
    },
    {
        "question": "Cách thức truyền thông nào sau đây mà tài nguyên được dành riêng trong suốt quá trình truyền dữ liệu?",
        "options": ["Cell switching", "Circuit switching", "Packet switching", "Các cách thức truyền thông trên đều sai"],
        "answer": "Circuit switching"
    },
        {
        "question": "Điều nào sau đây là đúng về giao thức mạng?",
        "options": ["Giao thức mạng là tập hợp các quy tắc, luật lệ hoặc định nghĩa truyền thông kết nối của 2 hay nhiều thiết bị mạng", "HTML là một giao thức thuộc về giao thức mạng", "Cả a và b đều đúng", "Cả a và b đều sai"],
        "answer": "Giao thức mạng là tập hợp các quy tắc, luật lệ hoặc định nghĩa truyền thông kết nối của 2 hay nhiều thiết bị mạng"
    },
    {
        "question": "Một packet có độ dài L vận chuyển từ AB qua 2 router (3 link) và có độ dài, tốc độ lan truyền, tốc độ truyền trên 3 đường link. Delay queue của router công thức nào sau đây tính delay end to end?",
        "options": ["a", "b", "c", "Cả 3 đều sai"],
        "answer": "Cả 3 đều sai"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về các ứng dụng HTTP, SMTP, FTP, BitTorrent?",
        "options": ["Cả 3 ứng dụng trên đều sử dụng chung kiến trúc peer to peer", "Cả 3 ứng dụng trên đều sử dụng chung dịch vụ ở tầng transport", "Cả a và b đều đúng", "Cả a và b đều sai"],
        "answer": "Cả a và b đều sai"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về kết nối HTTP sau: GET /cs453/index.html HTTP/1.1?",
        "options": ["Kiểu kết nối trên là kiểu kết nối bền vững", "Địa chỉ IP của thông tin 20040804", "Host là /cs456/index.html", "Cả a và b đều đúng"],
        "answer": "Kiểu kết nối trên là kiểu kết nối bền vững"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về giao thức TCP?",
        "options": ["Trong giao thức sequence number đại diện cho thứ tự số gói tin", "Trong giao thức TCP ack đại diện cho thứ tự số byte", "Trong giao thức TCP trường sequence number là một số có giới hạn", "Cả a, b, c đều đúng"],
        "answer": "Cả a, b, c đều đúng"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về cơ chế xử lý tắc nghẽn trong TCP?",
        "options": ["Khi đang trong giai đoạn CA thì mất gói tin dạng Dupack thì chuyển sang trạng thái slow start", "Khi trong giai đoạn slow start khi mất gói tin dạng timeout thì chuyển sang trạng thái CA", "A và b đều đúng", "A và b đều sai"],
        "answer": "A và b đều đúng"
    },
    {
        "question": "Truyền thông TCP ở 2 host A và B, host A đã nhận từ host B 300 bytes, host A đã gửi đến host B 400 bytes. Thông số seq và ack của gói tin TCP host A gửi đến host B là seq khởi tạo = 1. Chọn câu đúng?",
        "options": ["seq = 400, ACK = 301", "seq = 400, ACK = 300", "seq = 401, ACK = 301", "seq = 401, ACK = 300"],
        "answer": "seq = 401, ACK = 301"
    },
    {
        "question": "Điều nào sau đây là đúng về các trường trong IP v4 header?",
        "options": ["Trường source port và destination port đại diện cho thông số port nguồn và đích trong IP header", "Trường Flag có giá trị 000 khi gói tin là không bị fragment", "Trường identification là một trường số ID 32 bit đại diện cho một nhóm các gói tin được fragment từ một gói IP duy nhất", "Cả a, b, c đều đúng"],
        "answer": "Cả a, b, c đều đúng"
    },
    {
        "question": "Giả sử gói tin có địa chỉ IP nguồn đến host IP đích đi qua 3 router thì gói tin đi qua bao nhiêu interface và có bao nhiêu forward table?",
        "options": ["3, 3", "3, 2", "3, 8", "Cả a, b, c đều sai"],
        "answer": "3, 3"
    },
    {
        "question": "Điều nào sau đây là đúng về giao thức chuyển mạch ảo và giao thức chuyển mạch gói?",
        "options": ["Giao thức chuyển mạch gói là giao thức hướng kết nối", "Giao thức chuyển mạch ảo là giao thức phi kết nối tại tầng mạng", "Cả a và b đều đúng", "Cả a và b đều sai"],
        "answer": "Cả a và b đều sai"
    },
     {
        "question": "Điều nào sau đây là đúng khi nói về dịch vụ chuyển mạch gói?",
        "options": [
            "Luôn có một đường đi cố định từ địa chỉ nguồn đến đích",
            "Trước khi kết nối phải có quá trình bắt tay 3 bước",
            "Sử dụng địa chỉ IP để truyền thông qua mạng internet",
            "Cả a, b, c đều sai"
        ],
        "answer": "Cả a, b, c đều sai"
    },
    {
        "question": "Thiết bị switch có nhiệm vụ chính nào trong các nhiệm vụ sau?",
        "options": [
            "Routing",
            "Forward",
            "Cả a và b đều đúng",
            "Cả a và b đều sai"
        ],
        "answer": "Forward"
    },
    {
        "question": "Một gói datagram có thông số như sau identifier: 555, có số bytes 5200 được đi qua đường truyền có MTU = 1500 (biết rằng IP header có số byte là 20) xác định số byte data của trường total length của gói datagram cuối cùng trong nhóm IP fragment.",
        "options": [
            "700",
            "720",
            "740",
            "760"
        ],
        "answer": "740"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về địa chỉ IP sau đây 172.16.0.0.0/12?",
        "options": [
            "Đây là dãy IP public được mọi người thoải mái sử dụng trong mạng nội bộ",
            "Dãy địa chỉ IP này có thể được chia thành 16 dãy địa chỉ IP có số host bằng nhau",
            "Dãy địa chỉ IP này có địa chỉ broadcast là 255.255.255.0",
            "Dãy địa chỉ IP này có thể được đặt cho máy tính"
        ],
        "answer": "Dãy địa chỉ IP này có thể được đặt cho máy tính"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về thuật toán forwarding của router?",
        "options": [
            "So trùng phần bit trùng dài nhất",
            "Nếu không trùng phần nào trong forward table thì đi theo interface default",
            "Cả a và b đều đúng",
            "Cả a và b đều sai"
        ],
        "answer": "Cả a và b đều đúng"
    },
    {
        "question": "Một công ty được cấp một dãy địa chỉ đường mạng 200.24.17.0/20 công ty dùng đường mạng này để chia cho một phòng có tầm 350 máy tính. Đường mạng nào sau đây có thể là đường mạng có thể gán cho phòng máy này?",
        "options": [
            "200.24.22.0/23",
            "200.24.23.0/23",
            "200.24.25.0/23",
            "200.24.24.0/23"
        ],
        "answer": "200.24.22.0/23"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về giao thức NAT?",
        "options": [
            "Giao thức NAT sinh ra để tiết kiệm địa chỉ IP version 6",
            "Giao thức NAT dùng để chuyển đổi địa chỉ IP private thành địa chỉ IP public",
            "Giao thức NAT sử dụng thêm thông tin port xác định gói tin đến router đích",
            "Cả a, b, c đều đúng"
        ],
        "answer": "Cả a, b, c đều đúng"
    },
    {
        "question": "Trong giao thức CSMA/CD sau 5 lần bị collision thì xác suất thời gian random chọn K = 4 là bao nhiêu?",
        "options": [
            "1/4",
            "1/5",
            "1/20",
            "Kết quả khác"
        ],
        "answer": "1/20"
    },
    {
        "question": "Địa chỉ MAC broadcast có giá trị là bao nhiêu?",
        "options": [
            "FF-FF-FF-FF",
            "FF-FF-FF-FF-FF",
            "FF-FF-FF-FF-FF-FF",
            "FF-FF-FF-FF-FF-FF-FF"
        ],
        "answer": "FF-FF-FF-FF-FF-FF"
    },
    {
        "question": "Tính CRC của dữ liệu D= 1010101010 với đa thức sinh G= 10011",
        "options": [
            "0111",
            "0110",
            "0100",
            "1100"
        ],
        "answer": "0111"
    },
    {
        "question": "Tính internet checksum dữ liệu với các trường lần lượt như sau: 1 0000 0010, 11 00000100, 101 00000110, 101 00000110, 1001 00001010",
        "options": [
            "11001 00011110",
            "10111001 00011110",
            "1110100011100011",
            "1011001 00011110"
        ],
        "answer": "10111001 00011110"
    }, {
        "question": "Điều nào sau đây là đúng khi nói về dịch vụ chuyển mạch gói?",
        "options": [
            "Luôn có một đường đi cố định từ địa chỉ nguồn đến đích",
            "Trước khi kết nối phải có quá trình bắt tay 3 bước",
            "Sử dụng địa chỉ IP để truyền thông qua mạng internet",
            "Cả a, b, c đều sai"
        ],
        "answer": "Cả a, b, c đều sai"
    },
    {
        "question": "Thiết bị switch có nhiệm vụ chính nào trong các nhiệm vụ sau?",
        "options": [
            "Routing",
            "Forward",
            "Cả a và b đều đúng",
            "Cả a và b đều sai"
        ],
        "answer": "Forward"
    },
    {
        "question": "Một gói datagram có thông số như sau identifier: 555, có số bytes 5200 được đi qua đường truyền có MTU = 1500 (biết rằng IP header có số byte là 20) xác định số byte data của trường total length của gói datagram cuối cùng trong nhóm IP fragment.",
        "options": [
            "700",
            "720",
            "740",
            "760"
        ],
        "answer": "740"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về địa chỉ IP sau đây 172.16.0.0.0/12?",
        "options": [
            "Đây là dãy IP public được mọi người thoải mái sử dụng trong mạng nội bộ",
            "Dãy địa chỉ IP này có thể được chia thành 16 dãy địa chỉ IP có số host bằng nhau",
            "Dãy địa chỉ IP này có địa chỉ broadcast là 255.255.255.0",
            "Dãy địa chỉ IP này có thể được đặt cho máy tính"
        ],
        "answer": "Dãy địa chỉ IP này có thể được đặt cho máy tính"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về thuật toán forwarding của router?",
        "options": [
            "So trùng phần bit trùng dài nhất",
            "Nếu không trùng phần nào trong forward table thì đi theo interface default",
            "Cả a và b đều đúng",
            "Cả a và b đều sai"
        ],
        "answer": "Cả a và b đều đúng"
    },
    {
        "question": "Một công ty được cấp một dãy địa chỉ đường mạng 200.24.17.0/20 công ty dùng đường mạng này để chia cho một phòng có tầm 350 máy tính. Đường mạng nào sau đây có thể là đường mạng có thể gán cho phòng máy này?",
        "options": [
            "200.24.22.0/23",
            "200.24.23.0/23",
            "200.24.25.0/23",
            "200.24.24.0/23"
        ],
        "answer": "200.24.22.0/23"
    },
    {
        "question": "Điều nào sau đây là đúng khi nói về giao thức NAT?",
        "options": [
            "Giao thức NAT sinh ra để tiết kiệm địa chỉ IP version 6",
            "Giao thức NAT dùng để chuyển đổi địa chỉ IP private thành địa chỉ IP public",
            "Giao thức NAT sử dụng thêm thông tin port xác định gói tin đến router đích",
            "Cả a, b, c đều đúng"
        ],
        "answer": "Cả a, b, c đều đúng"
    },
    {
        "question": "Trong giao thức CSMA/CD sau 5 lần bị collision thì xác suất thời gian random chọn K = 4 là bao nhiêu?",
        "options": [
            "1/4",
            "1/5",
            "1/20",
            "Kết quả khác"
        ],
        "answer": "1/20"
    },
    {
        "question": "Địa chỉ MAC broadcast có giá trị là bao nhiêu?",
        "options": [
            "FF-FF-FF-FF",
            "FF-FF-FF-FF-FF",
            "FF-FF-FF-FF-FF-FF",
            "FF-FF-FF-FF-FF-FF-FF"
        ],
        "answer": "FF-FF-FF-FF-FF-FF"
    },
    {
        "question": "Tính CRC của dữ liệu D= 1010101010 với đa thức sinh G= 10011",
        "options": [
            "0111",
            "0110",
            "0100",
            "1100"
        ],
        "answer": "0111"
    },
    {
        "question": "Tính internet checksum dữ liệu với các trường lần lượt như sau: 1 0000 0010, 11 00000100, 101 00000110, 101 00000110, 1001 00001010",
        "options": [
            "11001 00011110",
            "10111001 00011110",
            "1110100011100011",
            "1011001 00011110"
        ],
        "answer": "10111001 00011110"
    }
]

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    if question_id >= len(questions):
        return redirect(url_for('result'))

    question = questions[question_id]
    
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == question['answer']:
            return render_template('feedback.html', correct=True, next_question=question_id + 1, question_text=question['question'])
        else:
            return render_template('feedback.html', correct=False, next_question=question_id + 1, correct_answer=question['answer'], question_text=question['question'])

    return render_template('quiz.html', question=question, question_id=question_id)

# @app.route('/result')
# def result():
#     return render_template('result.html')

# if __name__ == '__main__':
#     app.run(debug=True)
import random
@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
# def quiz(question_id):
#     # Shuffle the questions when the user starts the quiz
#     if question_id == 0:
#         random.shuffle(questions)
    
#     # Check if the question_id is valid
#     if question_id >= len(questions):
#         return redirect(url_for('result'))

#     question = questions[question_id]
    
#     # Shuffle the options for each question
#     options = question['options']
#     random.shuffle(options)
    
#     if request.method == 'POST':
#         selected_option = request.form.get('option')
#         if selected_option == question['answer']:
#             return render_template('feedback.html', correct=True, next_question=question_id + 1, question_text=question['question'])
#         else:
#             return render_template('feedback.html', correct=False, next_question=question_id + 1, correct_answer=question['answer'], question_text=question['question'])

#     return render_template('quiz.html', question=question, options=options, question_id=question_id)

@app.route('/result')
def result():
    total_questions = len(questions)
    score = session.get('score', 0)  # Get the score from the session
    return render_template('result.html', score=score, total_questions=total_questions)


if __name__ == '__main__':
    app.run(debug=True)