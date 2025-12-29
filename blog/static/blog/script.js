document.addEventListener('DOMContentLoaded', () => {
    const postCards = document.querySelectorAll('.post-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // 한 번 애니메이션 된 후에는 관찰을 중단하여 불필요한 재트리거 방지
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2 // 요소가 20% 보일 때 애니메이션 트리거
    });

    postCards.forEach(card => {
        observer.observe(card);
    });
});
