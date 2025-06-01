document.addEventListener('DOMContentLoaded', function() {
    // 初始化Swiper
    const initSwiper = () => {
        const swiper = new Swiper('.swiper', {
            loop: false,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
                renderBullet: function (index, className) {
                    return `<span class="${className}">${index + 1}</span>`;
                },
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: false,
            effect: 'slide',
            speed: 300,
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: 1,
            spaceBetween: 0,
            observer: true,
            observeParents: true,
            on: {
                init: function() {
                    this.slides.forEach(slide => {
                        const img = slide.querySelector('img');
                        if (img && img.complete) {
                            adjustImageSize(img);
                        }
                    });
                },
                slideChange: function() {
                    const activeSlide = this.slides[this.activeIndex];
                    const img = activeSlide.querySelector('img');
                    if (img) adjustImageSize(img);
                }
            }
        });

        // 监听图片加载完成事件
        document.querySelectorAll('.swiper-slide img').forEach(img => {
            if (!img.complete) {
                img.onload = function() {
                    this.style.opacity = 1;
                    adjustImageSize(this);
                    swiper.update();
                };
            }
        });

        return swiper;
    };

    // 调整图片大小以适应容器
    function adjustImageSize(img) {
        const container = img.closest('.swiper-slide');
        if (!container) return;

        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        const imgRatio = img.naturalWidth / img.naturalHeight;
        const containerRatio = containerWidth / containerHeight;

        if (imgRatio > containerRatio) {
            // 宽图，宽度100%，高度自适应
            img.style.width = '100%';
            img.style.height = 'auto';
        } else {
            // 高图，高度100%，宽度自适应
            img.style.width = 'auto';
            img.style.height = '100%';
        }
    }

    // 如果有图集，初始化Swiper
    let swiper;
    if (document.querySelector('.swiper')) {
        swiper = initSwiper();
        
        // 窗口大小改变时重新计算
        window.addEventListener('resize', function() {
            swiper.update();
            swiper.slides.forEach(slide => {
                const img = slide.querySelector('img');
                if (img) adjustImageSize(img);
            });
        });
    }

    // 下载全部图片功能
    const downloadAllBtn = document.getElementById('download-all');
    if (downloadAllBtn) {
        downloadAllBtn.addEventListener('click', function() {
            const images = document.querySelectorAll('.swiper-slide img');
            if (images.length === 0) return;

            let confirmed = confirm(`确定要下载全部 ${images.length} 张图片吗？`);
            if (!confirmed) return;

            let delay = 0;
            const downloadQueue = Array.from(images).map((img, index) => {
                return new Promise((resolve) => {
                    setTimeout(() => {
                        const link = document.createElement('a');
                        link.href = img.src;
                        link.download = `抖音图集_${index + 1}.jpg`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        resolve();
                    }, delay);
                    
                    delay += 1000; // 1秒间隔
                });
            });
            
            Promise.all(downloadQueue)
                .then(() => {
                    alert('所有图片下载完成！');
                })
                .catch((error) => {
                    console.error('下载出错:', error);
                    alert('部分图片下载失败，请重试');
                });
        });
    }
});