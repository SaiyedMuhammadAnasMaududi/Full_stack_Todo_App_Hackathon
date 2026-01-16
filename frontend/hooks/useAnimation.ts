import { useState, useEffect } from 'react';

interface AnimationState {
  isVisible: boolean;
  animationClass: string;
}

export const useAnimation = (trigger: boolean, animationType: 'fadeIn' | 'slideUp' | 'pop' | 'bounce' = 'fadeIn') => {
  const [state, setState] = useState<AnimationState>({
    isVisible: false,
    animationClass: ''
  });

  useEffect(() => {
    if (trigger) {
      // Trigger animation
      switch(animationType) {
        case 'slideUp':
          setState({
            isVisible: true,
            animationClass: 'animate-slide-up'
          });
          break;
        case 'pop':
          setState({
            isVisible: true,
            animationClass: 'animate-pop'
          });
          break;
        case 'bounce':
          setState({
            isVisible: true,
            animationClass: 'animate-bounce'
          });
          break;
        case 'fadeIn':
        default:
          setState({
            isVisible: true,
            animationClass: 'animate-fade-in'
          });
          break;
      }
    } else {
      // Fade out
      setState({
        isVisible: false,
        animationClass: 'animate-fade-out'
      });

      // Reset after animation completes
      const timer = setTimeout(() => {
        setState({
          isVisible: false,
          animationClass: ''
        });
      }, 300);

      return () => clearTimeout(timer);
    }
  }, [trigger, animationType]);

  return state;
};