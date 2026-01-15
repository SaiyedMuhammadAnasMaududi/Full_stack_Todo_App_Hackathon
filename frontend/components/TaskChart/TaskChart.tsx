'use client';

import { useEffect, useRef } from 'react';
import { Task } from '@/types';

interface TaskChartProps {
  tasks: Task[];
}

export default function TaskChart({ tasks }: TaskChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate stats
    const completedCount = tasks.filter(t => t.completed).length;
    const pendingCount = tasks.filter(t => !t.completed).length;

    // Draw pie chart
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 10;

    // Draw completed slice (green)
    if (completedCount > 0) {
      const completedPercentage = completedCount / tasks.length;
      const completedAngle = completedPercentage * 2 * Math.PI;

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, 0, completedAngle);
      ctx.closePath();
      ctx.fillStyle = '#10B981'; // green-500
      ctx.fill();

      // Draw label for completed
      const midAngle = completedAngle / 2;
      const labelX = centerX + Math.cos(midAngle) * (radius / 2);
      const labelY = centerY + Math.sin(midAngle) * (radius / 2);

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 14px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${Math.round(completedPercentage * 100)}%`, labelX, labelY);
    }

    // Draw pending slice (yellow)
    if (pendingCount > 0) {
      const pendingPercentage = pendingCount / tasks.length;
      const pendingAngle = pendingPercentage * 2 * Math.PI;
      const startAngle = tasks.some(t => t.completed) ? (completedCount / tasks.length) * 2 * Math.PI : 0;

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + pendingAngle);
      ctx.closePath();
      ctx.fillStyle = '#F59E0B'; // yellow-500
      ctx.fill();

      // Draw label for pending
      const midAngle = startAngle + pendingAngle / 2;
      const labelX = centerX + Math.cos(midAngle) * (radius / 2);
      const labelY = centerY + Math.sin(midAngle) * (radius / 2);

      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 14px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${Math.round(pendingPercentage * 100)}%`, labelX, labelY);
    }

    // Draw outline
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#E5E7EB'; // gray-200
    ctx.lineWidth = 2;
    ctx.stroke();
  }, [tasks]);

  return (
    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Task Distribution</h3>
      <div className="flex items-center justify-center">
        <canvas
          ref={canvasRef}
          width={200}
          height={200}
          className="w-48 h-48"
        />
        <div className="ml-6">
          <div className="flex items-center mb-2">
            <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
            <span className="text-sm font-medium text-gray-700">Completed: {tasks.filter(t => t.completed).length}</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-500 rounded mr-2"></div>
            <span className="text-sm font-medium text-gray-700">Pending: {tasks.filter(t => !t.completed).length}</span>
          </div>
        </div>
      </div>
    </div>
  );
}