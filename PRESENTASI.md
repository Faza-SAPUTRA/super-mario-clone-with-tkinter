# Alur Presentasi Super Mario

Urutan ini mengikuti alur program saat game dijalankan, bukan urutan nama
anggota. Campaign sekarang berjalan dari World 1-1 sampai World 3-1 dengan
total delapan level.

## 1. Ghazi - Launcher dan Persiapan Game

Folder kontribusi:

- `team_progress/ghazi/05_final/source/`

File utama:

- `classes/Launcher.py`
- `classes/Sound.py`
- `classes/Inventory.py`
- `classes/UiAssets.py`
- `compile.py`

Alur yang dijelaskan:

1. `main.py` memanggil `openLauncher()`.
2. Launcher membaca atau membuat `settings.json`.
3. User melihat preview tiga world, mengatur fullscreen, musik, dan SFX.
4. Tombol `START ADVENTURE` mengirim settings ke `setupGame()`.
5. Pygame, dashboard, audio, dan level engine diinisialisasi.

Catatan demo:

- Tombol world di launcher saat ini berfungsi sebagai preview.
- Campaign tetap dimulai dari World 1-1 sesuai `classes/Campaign.py`.
- Tunjukkan musik aktif dan slider volume, lalu mulai game.

Transisi:

"Setelah konfigurasi masuk ke Pygame, Kala akan menjelaskan bagaimana data
map diubah menjadi level yang bisa dimainkan."

## 2. Kala - Engine dan Desain Level

Folder kontribusi:

- `team_progress/kala/05_final/source/`

File utama:

- `classes/Level.py`
- `classes/Camera.py`
- `levels/Level1-1.json`
- `levels/Level1-2.json`
- `levels/Level1-3.json`
- `levels/Level1-4.json`
- `levels/Level2-1.json`
- `levels/Level2-2.json`
- `levels/Level2-3.json`
- `levels/Level3-1.json`

Alur yang dijelaskan:

1. `Level.loadLevel()` membaca file JSON.
2. `loadLayers()` membangun langit dan tanah.
3. `loadObjects()` memasang bush, cloud, pipe, warp pipe, dan flag.
4. `loadEntities()` memasang coin, box, Goomba, Koopa, dan power-up.
5. `drawLevel()` hanya menggambar bagian map yang terlihat oleh kamera.
6. `Camera.move()` mengikuti Mario dan berpindah langsung saat memakai warp pipe.
7. Setiap world memiliki flag sebagai tujuan akhir.

Data akhir campaign:

- World 1 terdiri dari empat level pengenalan dan canyon.
- World 2 terdiri dari coin ridge, pipe maze, dan shell run.
- World 3-1 adalah final gauntlet sepanjang 96 tile.

Transisi:

"Map sudah terbentuk. Berikutnya Fatir menjelaskan bagaimana Mario bergerak,
berinteraksi, dan mengubah flag menjadi progres campaign."

## 3. Fatir Zaidan - Gameplay dan Campaign

Folder kontribusi:

- `team_progress/fatir_zaidan/05_final/source/`

File utama:

- `entities/Mario.py`
- `classes/Campaign.py`
- `classes/QuestTracker.py`
- `classes/CheckpointManager.py`
- `main.py`

Alur yang dijelaskan:

1. `playCampaign()` menjalankan delapan level dari World 1-1 sampai World 3-1.
2. `Mario.update()` menjalankan gerak, gravitasi, collision, input, dan flag.
3. `checkFinishFlag()` mengubah `levelCompleted` menjadi `True`.
4. Setiap flag selain flag terakhir menampilkan `LEVEL COMPLETE`.
5. `prepareNextLevel()` mereset posisi dan state map, tetapi mempertahankan
   coin, inventory, power-up, dan progres quest.
6. Setelah flag World 3-1, `Campaign.goToNextLevel()` mengembalikan `False`.
7. Game menampilkan `CAMPAIGN COMPLETE`, final score, dan kembali ke launcher
   setelah Enter ditekan.

Bagian demo:

- Gerakkan Mario, lompat, ambil coin, dan kalahkan satu musuh.
- Gunakan warp pipe dengan tombol Down bila perlu mempercepat demo.
- Saat mencapai flag, jelaskan collision area flag.

Transisi:

"Coin dan event gameplay tadi juga dipakai oleh sistem bantuan. Rafa akan
menunjukkan shop, inventory, dan quest yang berjalan di tengah level."

## 4. Rafa Rabbani - Shop dan UI Pendukung

Folder kontribusi:

- `team_progress/rafa_rabbani/05_final/source/`

File utama:

- `classes/Shop.py`
- `classes/PygameShop.py`
- `README.md`
- `img/characters.gif`
- `img/Items.png`
- `img/pics.png`

Alur yang dijelaskan:

1. Tombol `B` memanggil `Mario.openShop()`.
2. Mode windowed memakai `Shop.py`, sedangkan fullscreen memakai
   `PygameShop.py` sebagai overlay dalam layar game yang sama.
3. Tab Shop menukar coin dengan Mushroom, Shield, Super Jump, Enemy Cleaner,
   atau checkpoint.
4. Tab Inventory menyimpan dan mengaktifkan item.
5. Tab Quests menampilkan progres coin, musuh, dan pembelian.
6. Tombol `CONTINUE LEVEL` atau tombol `B` menutup shop dan kembali ke game.

Bagian demo:

- Buka shop setelah memperoleh coin.
- Tunjukkan tiga tab.
- Beli atau gunakan Super Jump jika coin cukup.
- Tutup shop dan lanjutkan permainan.

## 5. Penutup Bersama - World 3-1 Sampai Tamat

Operator game melanjutkan sampai flag World 3-1.

Yang harus terlihat:

1. Flag terakhir berada dekat ujung map pada x = 93.
2. Menyentuh area tiang mengaktifkan `levelCompleted`.
3. Tidak ada world berikutnya.
4. Layar menampilkan:
   - `CAMPAIGN COMPLETE`
   - `ALL 8 LEVELS COMPLETE`
   - final score
   - `PRESS ENTER FOR LAUNCHER`
5. Tekan Enter untuk membuktikan alur kembali ke launcher.

Kalimat penutup:

"Game ini menggabungkan launcher Tkinter, runtime Pygame, level berbasis JSON,
delapan level campaign, serta companion shop. Campaign dinyatakan tamat setelah
Mario menyentuh flag di World 3-1."
