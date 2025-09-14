// --------------------------
//       Main js file
// --------------------------

(function ($) {
  ("use strict");
  // Preloader
  jQuery(window).on("load", function () {
    $(".preloader").delay(1600).fadeOut("slow");
  });

  $(".sidebar-button").on("click", function () {
    $(this).toggleClass("active");
  });

  document
    .querySelector(".sidebar-button")
    .addEventListener("click", () =>
      document.querySelector(".main-menu").classList.toggle("show-menu")
    );

  $(".menu-close-btn").on("click", function () {
    $(".main-menu").removeClass("show-menu");
  });

  // sidebar
  $(".right-sidebar-button").on("click", function () {
    $(".right-sidebar-menu").addClass("show-right-menu");
  });
  $(".right-sidebar-close-btn").on("click", function () {
    $(".right-sidebar-menu").removeClass("show-right-menu");
  });

  // Language Btn
  $(".language-btn").on("click", function (e) {
    let parent = $(this).parent();
    parent.find(".language-list").toggleClass("active");
    e.stopPropagation();
  });

  $(document).on("click", function (e) {
    if (!$(e.target).closest(".language-btn").length) {
      $(".language-list").removeClass("active");
    }
  });

  // niceSelect
  $(document).ready(function () {
    $("select").niceSelect();
  });

  // sticky header
  window.addEventListener("scroll", function () {
    const header = document.querySelector("header.header-area");
    header.classList.toggle("header-sticky", window.scrollY > 200);
  });

  // scroll up button
  document.addEventListener('DOMContentLoaded', function (event) {
    let offset = 50
    let circleContainer = document.querySelector('.circle-container')
    let circlePath = document.querySelector('.circle-container path')
    let pathLength = circlePath.getTotalLength()
    circlePath.style.transition = circlePath.style.WebkitTransition = 'none'
    circlePath.style.strokeDasharray = pathLength
    circlePath.style.strokeDashoffset = pathLength
    circlePath.getBoundingClientRect()
    circlePath.style.transition = circlePath.style.WebkitTransition =
      'stroke-dashoffset 10ms linear'

    let updateLoader = () => {
      let scrollTop = window.scrollY
      let docHeight = document.body.offsetHeight
      let winHeight = window.innerHeight
      let height = docHeight - winHeight
      let progress = pathLength - (scrollTop * pathLength) / height
      circlePath.style.strokeDashoffset = progress

      if (scrollTop > offset) {
        circleContainer.classList.add('active')
      } else {
        circleContainer.classList.remove('active')
      }
    }
    circleContainer.onclick = function () {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    window.onscroll = () => {
      updateLoader()
    }
    updateLoader()
  })

  // Video Popup

  $('[data-fancybox="gallery"]').fancybox({
    buttons: [
      "close"
    ],
    loop: false,
    protect: true
  });
  $('.video-player').fancybox({
    buttons: [
      "close"
    ],
    loop: false,
    protect: true
  });


  // smooth scroll start
  function scrollTo() {
    $(window).scrollTo({ top: 0, behavior: "smooth" });
  }
  // smooth scroll end

  // right sidebar start
  $(".right-sidebar-button").on("click", function () {
    $(".right-sidebar-menu").addClass("show-right-menu");
  });
  $(".right-sidebar-close-btn").on("click", function () {
    $(".right-sidebar-menu").removeClass("show-right-menu");
  });

  jQuery(".dropdown-icon").on("click", function () {
    jQuery(this).toggleClass("active").next("ul").slideToggle();
    jQuery(this).parent().siblings().children("ul").slideUp();
    jQuery(this).parent().siblings().children(".active").removeClass("active");
  });
  
  //  right sidebar end

  //Scroll Down Button
  const scrollBtn = document.querySelector("#scroll-btn");
  if (scrollBtn) {
    scrollBtn.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector("#scroll-section").scrollIntoView({
        behavior: "smooth",
      });
    });
  }

  // calender
  $(function () {
    $('input[name="inOut"]').daterangepicker(
      {
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 2023,
        maxYear: 2025,
        locale: {
          format: "DD-MMM-YYYY",
        },
      },
      function (start, end, label) {
        var years = moment().diff(start, "years");
      }
    );

    $('input[name="daterange"]').daterangepicker(
      {
        opens: "left",
        minYear: "2023",
        maxYear: "2025",
        locale: {
          format: "DD-MMM",
        },
      },
      function (start, end, label) {
        console.log(
          "A new date selection was made: " +
          start.format("YYYY-MM-DD") +
          " to " +
          end.format("YYYY-MM-DD")
        );
      }
    );
  });

	// Handle click on the input item
	$('.select-input').on("click", function () {
		$('.custom-select-wrap').toggleClass('active');
	});
	//Destination-dropdown
	$(document).on("click", '.destination-dropdown-icon', function (e) {
		e.stopPropagation();
		$(this).next(".destination-wrap").toggleClass("active");
		$(this).parents('.destination-column').siblings().children('.destination-dropdown-card').children('.destination-wrap').removeClass('active');
	});
	$(document).on("click", function (e) {
		if (!$(e.target).closest(".destination-wrap").length) {
			$(".destination-wrap").removeClass("active");
		}
	});

	$('.searchbox-input').each(function () {
		var $container = $(this);
		$container.find('.option-list li').on("click", function () {
			var destinationText = $(this).find('.destination h6, h6').text();
			$container.find('.select-input input').val(destinationText);
			$container.find('.custom-select-wrap').removeClass('active');
		});
		$(document).on("click", function (event) {
			if (!$(event.target).closest($container).length) {
				$container.find('.custom-select-wrap').removeClass('active');
			}
		});
		$container.find('.custom-select-search-area input').on('input', function () {
			var searchText = $(this).val().toLowerCase();
			$container.find('.option-list li').each(function () {
				var destinationText = $(this).find('.destination h6').text().toLowerCase();
				if (destinationText.includes(searchText)) {
					$(this).show();
				} else {
					$(this).hide();
				}
			});
		});
	});

	//select2
	$(".deatination_drop").select2({
		closeOnSelect: true,
		width: 'resolve'
	});


  $(".location-area").each(function () {
    var dealName = $(this).children(".location-list");

    if (dealName.width() >= $(this).width()) {
      dealName.addClass("scrollTextAni");
    }
  });


  $(document).on("click", ".toggle- ord", function() {
    $(this).toggleClass("bi-eye bi-eye-slash");
    let input = $(this).siblings("input");
    input.attr("type", input.attr("type") === "password" ? "text" : "password");
  });

  //  counter
  $('.counter').counterUp({
    delay: 10,
    time: 1500
  });



  // =================
  // Country Card 
  // =================

  // Initialize the first child as active on page load
  $('.country-area ul li:first-child').addClass('active');

  // Mouse enter event for country-area div

  // Mouse leave event for country-area div
  $('.country-area').on("mouseleave", function () {
    // Remove active class from all li elements except the first child
    $('.country-area ul li:not(:first-child)').removeClass('active');
    // Add active class to the first child
    $('.country-area ul li:first-child').addClass('active');
  });
  // Hover event for li elements
  $('.country-area ul li').on(
    {
      mouseenter: function () {
        // Add active class to the current li and remove from siblings
        $(this).addClass('active').siblings().removeClass('active');
      }
    }
  );

  //Quantity Increment
  
  $(".quantity__minus").on("click", function (e) {
    e.preventDefault();
    var input = $(this).siblings(".quantity__input");
    var value = parseInt(input.val(), 10);
    if (value > 1) {
      value--;
    }
    input.val(value.toString().padStart(2, "0"));
  });
  $(".quantity__plus").on("click", function (e) {
    e.preventDefault();
    var input = $(this).siblings(".quantity__input");
    var value = parseInt(input.val(), 10);
    value++;
    input.val(value.toString().padStart(2, "0"));
  });

  //Quantity Increment Guest
  $(".guest-quantity__minus").on("click", function (e) {
    let type = $(this).data('type');
    e.preventDefault();
    var input = $(this).siblings(".quantity__input");
    var value = parseInt(input.val(), 10);

    if (type == 'adult') {
      if (value > 1) {
        value--;
        $("#adult-qty").text(value.toString())
        //    $("#adullt_select_qty").val(value.toString());
      }
    } else if (type == 'child') {
      if (value > 0) {
        value--;
        $("#child-qty").text(value.toString())
        // $("#child_seelct_qty").val(value.toString());
      }
    }
    input.val(value == 0 ? value : value.toString());
  });

  $(".guest-quantity__plus").on("click", function (e) {
    e.preventDefault();
    let type = $(this).data('type');
    var input = $(this).siblings(".quantity__input");
    var value = parseInt(input.val(), 10);
    value++;
    if (type == 'adult') {
      $("#adult-qty").text(value.toString())
      //   $("#adullt_select_qty").val(value.toString());
    } else if (type == 'child') {
      $("#child-qty").text(value.toString())
      // $("#child_seelct_qty").val(value.toString());
    }
    input.val(value.toString());
  });

  // container-fluid-sticky-right
  function containerFull() {
    var container = document.querySelector('.container');
    var distanceFromWindow = container.offsetLeft;
    var containerStyles = window.getComputedStyle(container);
    var paddingOneSide = parseInt(containerStyles.paddingLeft)

    document.querySelectorAll('.container-fluid-sticky-right').forEach((el) => {
      el.style.marginLeft = distanceFromWindow + 'px';
      el.style.paddingLeft = paddingOneSide + 'px';
    });
  }
  containerFull();
  window.addEventListener('resize', containerFull);

  // swiper js
  var swiper = new Swiper(".tour-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".tour-card-next",
      prevEl: ".tour-card-prev",
    },
    pagination: {
      el: ".tour-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 4,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 4,
      },
    }
  });

  var swiper = new Swiper(".tour-card-slider-four", {
    slidesPerView: 1,
    speed: 1500,
    clickable: true,
    loop: true,
    spaceBetween: 25,
    autoplay: {
      delay: 1500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".popular-card-next",
      prevEl: ".popular-card-prev",
    },
    pagination: {
      el: ".tour-pagination",
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 'auto',
      },
      576: {
        slidesPerView: 'auto',
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 'auto',
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 'auto',
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 'auto',
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 'auto',
      },
    }
  });
// ................
  var swiper = new Swiper(".testimonial-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    loop: true,
    effect: 'fade',             // Use the fade effect
    fadeEffect: {
      crossFade: true,           // Enable cross-fade transition
    },
    autoplay: {
      delay: 1000, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".testimonial-slider-next",
      prevEl: ".testimonial-slider-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 1,
      },
    }
  });
  // testimonial Slider
	var swiper = new Swiper(".testimonial-card-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		loop: true,
    effect: 'fade',             // Use the fade effect
		fadeEffect: {
		crossFade: true           // Enable cross-fade transition
		},
		autoplay: {
			delay: 2000, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
    navigation: {
      nextEl: ".testimonial-slider-next",
      prevEl: ".testimonial-slider-prev",
    },
	});

  var swiper = new Swiper(".testimonial-card-slider-three", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    loop: true,
    effect: 'fade',             // Use the fade effect
		fadeEffect: {
		crossFade: true           // Enable cross-fade transition
		},
		autoplay: {
			delay: 1500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
    navigation: {
      nextEl: ".testimonial-slider-next",
      prevEl: ".testimonial-slider-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 1,
      },
    }
  });

  var swiper = new Swiper(".testimonial-wrap-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    loop: true,
    effect: 'fade',             // Use the fade effect
    fadeEffect: {
      crossFade: true,           // Enable cross-fade transition
    },
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".slider-next",
      prevEl: ".slider-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 1,
      },
    }
  });

  var swiper = new Swiper(".banner-slider-three", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 30,
    loop: true, // Ensures infinite loop
    watchOverflow: true, // Prevents hiding pagination if slides are less
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      dynamicBullets: false, // Set to false to ensure all bullets appear
      renderBullet: function (index, className) {
        return '<span class="' + className + '">' + (index + 1).toString().padStart(2, "0") + "</span>";
      },
    },
    navigation: {
      nextEl: ".banner-slider-next",
      prevEl: ".banner-slider-prev",
    },
    autoplay: {
      delay: 1500,
      disableOnInteraction: false,
    },
    on: {
      init: function () {
        this.autoplay.start(); // Ensures autoplay starts properly
      },
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 2,
        spaceBetween: 25,
      },
      1200: {
        slidesPerView: 2,
        spaceBetween: 35,
      },
      1400: {
        slidesPerView: 2.8,
        spaceBetween: 35,
      },
    }
  });

  var swiper = new Swiper(".destination-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    pagination: {
      el: ".destination-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
      },
      1400: {
        slidesPerView: 4,
        spaceBetween: 15,
      },
    }
  });

  var swiper = new Swiper(".packages-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".packages-card-next",
      prevEl: ".packages-card-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 4,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 4,
      },
    }
  });

  var swiper = new Swiper(".packages-card-slider-two", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".packages-card-next",
      prevEl: ".packages-card-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 3,
      },
    }
  });
  
  var swiper = new Swiper(".packages-card-slider-three", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".packages-card-next",
      prevEl: ".packages-card-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 3,
      },
    }
  });

  var swiper = new Swiper(".teams-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".teams-card-next",
      prevEl: ".teams-card-prev",
    },
    pagination: {
      el: ".team-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 4,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 4,
      },
    }
  });

  var swiper = new Swiper(".visa-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".visa-card-next",
      prevEl: ".visa-card-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 4,
      },
    }
  });

  var swiper = new Swiper(".blog-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".blog-card-next",
      prevEl: ".blog-card-prev",
    },

    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 2,
      },
    }
  });

  var swiper = new Swiper(".promotion-card-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".tour-card-next",
      prevEl: ".tour-card-prev",
    },
    pagination: {
      el: ".promotion-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 2,
      },
    }
  });


  var swiper = new Swiper(".tour-guide-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".tour-guide-next",
      prevEl: ".tour-guide-prev",
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 4,
      },
    }
  });

  var swiper = new Swiper(".tour-package-slider-four", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".tour-package-next",
      prevEl: ".tour-package-prev",
    },
    pagination: {
      el: ".tour-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      992: {
        slidesPerView: 2,
        spaceBetween: 15,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1400: {
        slidesPerView: 3,
      },
    }
  });

  var swiper = new Swiper(".visa-project-slider", {
    slidesPerView: 1,
    speed: 1500,
    spaceBetween: 25,
    autoplay: {
      delay: 1500, // Autoplay duration in milliseconds
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".project-slider-next",
      prevEl: ".project-slider-prev",
    },
    pagination: {
      el: ".visa-pagination",
      clickable: true,
    },
    breakpoints: {
      280: {
        slidesPerView: 1,
      },
      386: {
        slidesPerView: 1,
      },
      576: {
        slidesPerView: 1,
        spaceBetween: 15,
      },
      768: {
        slidesPerView: 2,
      },
      992: {
        slidesPerView: 2,
      },
      1200: {
        slidesPerView: 2,
      },
      1400: {
        slidesPerView: 2.6,
      },
    },
  });
  
// testimonial-slider-four
  var swiper = new Swiper(".testimonial-slider-four", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		// loop: true,
    effect: 'fade',             // Use the fade effect
		fadeEffect: {
		  crossFade: true           // Enable cross-fade transition
		},
		autoplay: {
			delay: 1500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
		nextEl: ".visa-next-four",
		prevEl: ".visa-preview-four",
		},
	});


  // Product Slider
  const sliders = document.querySelectorAll('.product-img-slider');
  sliders.forEach((slider) => {
    const nextBtn = slider.parentElement.querySelector('.product-stand-next');
    const prevBtn = slider.parentElement.querySelector('.product-stand-prev');

    const swiper = new Swiper(slider, {
      slidesPerView: 1,
      speed: 1500,
      spaceBetween: 10,
      loop: true,
      autoplay: {
        delay: 2000, // Autoplay duration in milliseconds
        disableOnInteraction: false,
      },
      pagination: {
        el: ".product-pagination",
        clickable: true,
      },
   
    });
 
  });
 

  //see all image view 
  var startedFromIndexPage = false;
  $(document).on("click", '.StartSlideShowFirstImage', function () {
    startedFromIndexPage = true;
    $('a[data-fancybox="images"]').first().trigger('click');
    $.fancybox.getInstance().SlideShow.toggle();
  })

  $('[data-fancybox="images"]').fancybox({
    fullScreen: {
      autoStart: true,
    },
    buttons: ['slideShow', 'share', 'close'],
    onSlideShowChange: function (instance, current, active) {
      console.info('SlideShow active? ' + active);
      if (active && !startedFromIndexPage) {
        instance.next();
      }
      startedFromIndexPage = false;
    }
  });

  // progress line
  if ($('.progress-bar').length) {
    $(window).on('scroll', function() {
      let scroll = $(window).scrollTop();
      let oTop = $('.progress-bar').offset().top - window.innerHeight;
      if (scroll > oTop) {
        $(".progress-bar").addClass("progressbar-active");
      } else {
        $(".progress-bar").removeClass("progressbar-active");
      }
    });
  }
  
 
// wow js
$(window).on('load', function () {
  new WOW().init();
  window.wow = new WOW({
      boxClass: 'wow',
      animateClass: 'animated',
      offset: 0,
      mobile: true,
      live: true,
      offset: 80
  })
  window.wow.init();
});



})(jQuery);


