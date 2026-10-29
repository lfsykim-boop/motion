# ㅇ 속으로

10월 아침의 고요를 찢는 30초 키네틱 타이포 모션 그래픽. [HyperFrames](https://github.com/heygen-com/hyperframes)로 HTML을 MP4로 렌더링했다.

- 영상: [`docs/october-morning.mp4`](docs/october-morning.mp4) · 웹 페이지: https://lfsykim-boop.github.io/motion/
- 기획: [`STORYLINES.md`](STORYLINES.md) · 연출 스펙: [`SPEC.md`](SPEC.md) · 검토 기록: [`REVIEW.md`](REVIEW.md)

## 다시 렌더링하기

Node.js 22+, FFmpeg가 필요하다.

```bash
npx hyperframes skills update   # 처음 한 번
# 효과음은 라이선스상 저장소에 넣지 않았다. HyperFrames 기본 효과음에서 복사한다.
#   whoosh, whoosh-cinematic, impact-bass-1, impact-bass-2, riser, click-soft → assets/sfx/
python build_scenes.py          # compositions/*.html, index.html 생성
npx hyperframes preview         # 미리보기
npx hyperframes render -o renders/october-morning.mp4
```

## 크레딧

- 음악: "Fresh Morning" by howserg — https://www.jamendo.com/track/1277167 — [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). 14.155초부터 26.25초 구간을 잘라 페이드와 음량 정규화(-14 LUFS)를 적용했다.
- 글꼴: Pretendard © Kil Hyung-jin — SIL Open Font License 1.1 (`assets/fonts/LICENSE-Pretendard.txt`)
- 효과음: HyperFrames 기본 라이브러리(Pixabay Content License)
