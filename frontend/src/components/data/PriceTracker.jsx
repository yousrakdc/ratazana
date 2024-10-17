import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import './PriceTracker.css';

Chart.register(...registerables);

const PriceTracker = ({ priceData }) => {
    const chartRef = useRef(null);
    const chartInstanceRef = useRef(null);

    useEffect(() => {
        if (!priceData || priceData.length === 0) return;

        const ctx = chartRef.current.getContext('2d');

        if (chartInstanceRef.current) {
            chartInstanceRef.current.destroy();
        }

        chartInstanceRef.current = new Chart(ctx, {
            type: 'line',
            data: {
                labels: priceData.map(item => item.date),
                datasets: [{
                    label: 'Price History',
                    data: priceData.map(item => item.price),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'category',
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price'
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false
            }
        });

        return () => {
            if (chartInstanceRef.current) {
                chartInstanceRef.current.destroy();
            }
        };
    }, [priceData]);

    return (
        <div className="price-tracker-container">
            <canvas ref={chartRef} />
        </div>
    );
};

export default PriceTracker;
