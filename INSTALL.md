# CoinVoice - Hướng dẫn cài đặt
## [Cài đặt Python 3.8.3](https://www.python.org/downloads/)
- Ở phần ```Optional Features```, nhớ chọn pip (nếu không có phần ```Optional Features``` thì tiếp tục như bình thường)
- Nhớ chọn ``Add Python xx to PATH``
## [Tải mã nguồn CoinVoice](https://github.com/dvbui/CoinVoice)
- Nhấn ```Clone or download```, sau đó chọn ```Download ZIP```
- Giải nén mã nguồn vào thư mục nào đó
## Cài đặt thư viện Discord
- Mở ```Command Prompt``` tại thư mục chứa mã nguồn (thư mục có tệp ```coinvoice.py```) ([hướng dẫn](https://www.youtube.com/watch?v=JLqIkPfU_0U))
- Gõ lệnh ```pip install -r requirements.txt```
## Tạo bot
- Vào ```https://discord.com/developers/applications```
- Nhấn ```New Application```. Đặt tên cho application (```CoinVoice``` chẳng hạn).
- Trong phần ```Settings```, tạo một con bot. Sau đó nhấn ```Click to reveal token``` rồi lưu dòng chữ đó vào tệp ```client_token.txt``` trong thư mục mã nguồn (nếu không có tệp đó thì ta có thể tự tạo) 
- Ta có thể đặt Avatar cho bot ở phần ```Icon```
## Sửa các tệp chứa thông tin trong thư mục mã nguồn
### Tệp ```help_message.txt```
Tệp này chứa thông tin được gửi khi người dùng gõ lệnh ```coin help```. Thường ta không cần sửa tệp này
### Tệp ```role_menu.txt```
Tệp này gồm nhiều dòng, mỗi dòng gồm hai số nguyên (không phải số thập phân). Số nguyên đầu tiên của mỗi dòng là mã role. Số nguyên thứ hai của mỗi dòng là giá của role đó.

Để lấy mã role, trong phòng chat trên Discord, ta có thể gõ lệnh ```\@tênrole```. Dòng số được gửi về là mã role (đừng chép cả những kí tự thừa như ```<```, ```>```, ...)

### Tệp ```voice_channel.txt```
Tệp này gồm nhiều dòng, mỗi dòng gồm một số nguyên là mã phòng voice chat. Để lấy mã phòng voice chat, ta vào trình duyệt, vào phòng chat, rồi chép dòng số ở cuối đường link (sau dấu ```\```)
### Tệp ```user_data_file.json```
Tệp này chứa thông tin người dùng và số tiền hiện có. Để đưa số tiền của mỗi người về 0, thay thông tin trong tệp bằng ```{}```
### Tệp ```coinvoice.py```
Ở dòng 15, 16 có
```
ITERATION = 1
UNIT_MONEY = 1
```
Dòng này có nghĩa mỗi ```ITERATION``` giây thì mỗi người trong phòng chat nhận được ```UNIT_MONEY``` đồng.
Ta có thể thay các giá trị ```1``` bằng các số nguyên khác cho phù hợp. Ví dụ nếu ta muốn mỗi 60 giây thì mỗi người trong phòng chat nhận được 2 đồng thì ta thay bằng 
```
ITERATION = 60
UNIT_MONEY = 2
```
## Chạy bot
Mở Command Prompt trong thư mục mã nguồn, rồi gõ lệnh
```python coinvoice.py```
Nếu xuất hiện lỗi gì thì bạn có thể thông báo cho mình.
Bot nên được chạy trên một máy có kết nối mạng 24 giờ mỗi ngày, và nên được tắt đi bật lại khoảng một lần mỗi ngày (có thể chọn lúc ít người dùng để khởi động lại)
