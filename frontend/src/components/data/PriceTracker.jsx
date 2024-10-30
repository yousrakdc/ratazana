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

        // Destroy the existing chart instance if it exists
        if (chartInstanceRef.current) {
            chartInstanceRef.current.destroy();
        }

        // Create a new chart instance with updated data
        chartInstanceRef.current = new Chart(ctx, {
            type: 'line',
            data: {
                labels: priceData.map(item => {
                    const date = new Date(item.date);
                    return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: '2-digit' });
                }),
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
                            text: 'Date',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        }
                    },
                    y: {
                        min: 0,
                        max: 300,
                        title: {
                            display: true,
                            text: 'Price',
                            color: 'white'
                        },
                        ticks: {
                            color: 'white'
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    }
                }
            }
        });

        // Cleanup function to destroy the chart instance on unmount
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
