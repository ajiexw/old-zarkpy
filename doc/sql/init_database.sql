CREATE USER songshu IDENTIFIED BY '4658721ddfcb2fff651bd369ea632200c4c62219';
GRANT ALL PRIVILEGES ON songshu.* TO songshu@'localhost' IDENTIFIED BY '4658721ddfcb2fff651bd369ea632200c4c62219';
GRANT ALL PRIVILEGES ON songshu_test.* TO songshu@'localhost' IDENTIFIED BY '4658721ddfcb2fff651bd369ea632200c4c62219';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS songshu;
CREATE DATABASE IF NOT EXISTS songshu_test;
