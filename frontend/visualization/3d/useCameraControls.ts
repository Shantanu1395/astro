// Camera Controls Hook
import { useState, useCallback, useRef, useEffect } from 'react';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';

interface CameraState {
  position: THREE.Vector3;
  target: THREE.Vector3;
  distance: number;
  isFreeMoveMode: boolean;
}

interface UseCameraControlsOptions {
  initialPosition?: THREE.Vector3;
  initialTarget?: THREE.Vector3;
  enableKeyboardControls?: boolean;
  movementSpeed?: number;
  transitionDuration?: number;
}

export const useCameraControls = (options: UseCameraControlsOptions = {}) => {
  const {
    initialPosition = new THREE.Vector3(0, 50, 100),
    initialTarget = new THREE.Vector3(0, 0, 0),
    enableKeyboardControls = true,
    movementSpeed = 10,
    transitionDuration = 1000
  } = options;

  const { camera, scene } = useThree();
  const [cameraState, setCameraState] = useState<CameraState>({
    position: initialPosition.clone(),
    target: initialTarget.clone(),
    distance: initialPosition.distanceTo(initialTarget),
    isFreeMoveMode: false
  });

  const animationRef = useRef<number | null>(null);
  const raycaster = useRef(new THREE.Raycaster());
  const mouse = useRef(new THREE.Vector2());

  // Update camera state
  const updateCameraState = useCallback(() => {
    setCameraState(prev => ({
      ...prev,
      position: camera.position.clone(),
      distance: camera.position.distanceTo(prev.target)
    }));
  }, [camera]);

  // Smooth camera transition
  const transitionCamera = useCallback((
    newPosition: THREE.Vector3,
    newTarget: THREE.Vector3,
    duration: number = transitionDuration
  ) => {
    const startPosition = camera.position.clone();
    const startTarget = cameraState.target.clone();
    const startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function (ease out cubic)
      const easeProgress = 1 - Math.pow(1 - progress, 3);

      // Interpolate position
      camera.position.lerpVectors(startPosition, newPosition, easeProgress);
      
      // Update target
      const currentTarget = new THREE.Vector3().lerpVectors(startTarget, newTarget, easeProgress);
      
      // Update state
      setCameraState(prev => ({
        ...prev,
        position: camera.position.clone(),
        target: currentTarget,
        distance: camera.position.distanceTo(currentTarget)
      }));

      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate);
      } else {
        updateCameraState();
      }
    };

    // Cancel any existing animation
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    animate();
  }, [camera, cameraState.target, transitionDuration, updateCameraState]);

  // Focus on a specific target
  const focusOnTarget = useCallback((target: THREE.Vector3, distance?: number) => {
    const currentDirection = new THREE.Vector3()
      .subVectors(camera.position, cameraState.target)
      .normalize();
    
    const targetDistance = distance || Math.max(20, Math.min(200, cameraState.distance));
    const newPosition = new THREE.Vector3()
      .addVectors(target, currentDirection.multiplyScalar(targetDistance));

    transitionCamera(newPosition, target);
  }, [camera, cameraState, transitionCamera]);

  // Focus on Earth
  const focusOnEarth = useCallback(() => {
    focusOnTarget(new THREE.Vector3(0, 0, 0), 50);
  }, [focusOnTarget]);

  // Focus on Sun
  const focusOnSun = useCallback(() => {
    // Sun position from CelestialSphere component
    const sunPosition = new THREE.Vector3(10, 0, 0);
    focusOnTarget(sunPosition, 30);
  }, [focusOnTarget]);

  // Focus on Moon
  const focusOnMoon = useCallback(() => {
    // Moon orbits Earth, so we'll focus on Earth's vicinity
    focusOnTarget(new THREE.Vector3(0, 0, 0), 15);
  }, [focusOnTarget]);

  // Focus on Jupiter
  const focusOnJupiter = useCallback(() => {
    // Jupiter position from CelestialSphere component
    const jupiterPosition = new THREE.Vector3(-44, 0, 0);
    focusOnTarget(jupiterPosition, 80);
  }, [focusOnTarget]);

  // Reset camera to default position
  const resetCamera = useCallback(() => {
    transitionCamera(initialPosition, initialTarget);
    setCameraState(prev => ({ ...prev, isFreeMoveMode: false }));
  }, [initialPosition, initialTarget, transitionCamera]);

  // Toggle free movement mode
  const toggleFreeMovement = useCallback(() => {
    setCameraState(prev => ({
      ...prev,
      isFreeMoveMode: !prev.isFreeMoveMode
    }));
  }, []);

  // Handle mouse click for focusing
  const handleMouseClick = useCallback((event: MouseEvent) => {
    if (event.detail === 2) { // Double click
      // Convert mouse position to normalized device coordinates
      mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.current.y = -(event.clientY / window.innerHeight) * 2 + 1;

      // Cast ray from camera through mouse position
      raycaster.current.setFromCamera(mouse.current, camera);
      const intersects = raycaster.current.intersectObjects(scene.children, true);

      if (intersects.length > 0) {
        const point = intersects[0].point;
        focusOnTarget(point);
      }
    }
  }, [camera, scene, focusOnTarget]);

  // Keyboard controls
  useEffect(() => {
    if (!enableKeyboardControls) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      switch (event.code) {
        case 'KeyR':
          resetCamera();
          event.preventDefault();
          break;
        case 'KeyE':
          focusOnEarth();
          event.preventDefault();
          break;
        case 'KeyF':
          toggleFreeMovement();
          event.preventDefault();
          break;
        case 'Digit1':
          focusOnSun();
          event.preventDefault();
          break;
        case 'Digit2':
          focusOnMoon();
          event.preventDefault();
          break;
        case 'Digit3':
          focusOnJupiter();
          event.preventDefault();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('click', handleMouseClick);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('click', handleMouseClick);
    };
  }, [
    enableKeyboardControls,
    resetCamera,
    focusOnEarth,
    focusOnSun,
    focusOnMoon,
    focusOnJupiter,
    toggleFreeMovement,
    handleMouseClick
  ]);

  // Cleanup animation on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return {
    cameraState,
    focusOnTarget,
    focusOnEarth,
    focusOnSun,
    focusOnMoon,
    focusOnJupiter,
    resetCamera,
    toggleFreeMovement,
    transitionCamera,
    updateCameraState
  };
};
