void setup() {
  // 14.4 MHZ on PA8
  // Enable clocks
  RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;   // Enable GPIOA clock
  RCC->APB2ENR |= RCC_APB2ENR_AFIOEN;   // Enable AFIO clock
  RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;   // Enable TIM1 clock

  // Set PA8 to Alternate Function Push-Pull (AF PP)
  GPIOA->CRH &= ~(GPIO_CRH_CNF8 | GPIO_CRH_MODE8);
  GPIOA->CRH |= (GPIO_CRH_CNF8_1 | GPIO_CRH_MODE8); // AF PP, output 50MHz

  // Reset TIM1
  TIM1->CR1 = 0;
  TIM1->CR2 = 0;
  TIM1->SMCR = 0;
  TIM1->DIER = 0;

  // Set PWM frequency to 12 MHz
  TIM1->PSC = 0;       // Prescaler = 0 (no division)
  TIM1->ARR = 5 - 1;   // ARR = 4 → 72MHz / 5 = 14.4 MHz
  TIM1->CCR1 = 2;      // 50% duty (2 out of 4)

  // Set PWM mode 1 on CH1 and enable preload
  TIM1->CCMR1 = TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2 | TIM_CCMR1_OC1PE;

  TIM1->CCER |= TIM_CCER_CC1E;   // Enable output on CH1
  TIM1->BDTR |= TIM_BDTR_MOE;    // Main output enable (advanced timers only)

  TIM1->CR1 |= TIM_CR1_ARPE;     // Enable auto-reload preload
  TIM1->EGR |= TIM_EGR_UG;       // Force update
  TIM1->CR1 |= TIM_CR1_CEN;      // Start timer
}

void loop() {
}
