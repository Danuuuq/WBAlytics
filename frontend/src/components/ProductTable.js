import React from 'react';

const ProductTable = ({ products = [], sortBy, setSortBy, setFilters }) => {
  const handleSort = (field) => {
    setSortBy((prev) => {
      const newDirection = prev.field === field && prev.direction === 'asc' ? 'desc' : 'asc';
      return { field, direction: newDirection };
    });

    // обновляем фильтры (и тем самым триггерим fetchProducts заново)
    setFilters((prev) => ({
      ...prev,
      sort_by: field,
      sort_dir: prev.sort_by === field && prev.sort_dir === 'asc' ? 'desc' : 'asc',
    }));
  };

  const renderArrow = (field) => {
    if (sortBy.field !== field) return '';
    return sortBy.direction === 'asc' ? ' 🔼' : ' 🔽';
  };

  const formatPrice = (price) => {
    const numPrice = Number(price);
    return isNaN(numPrice) ? '0₽' : `${numPrice.toLocaleString('ru-RU')}₽`;
  };

  const formatRating = (rating) => {
    const numRating = Number(rating);
    return isNaN(numRating) ? '0' : numRating.toFixed(1);
  };

  const formatReviewCount = (count) => {
    const numCount = Number(count);
    return isNaN(numCount) ? '0' : numCount.toLocaleString('ru-RU');
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table
        style={{
          width: '100%',
          marginTop: 20,
          borderCollapse: 'collapse',
          border: '1px solid #ddd',
        }}
      >
        <thead>
          <tr style={{ backgroundColor: '#f5f5f5' }}>
            <th onClick={() => handleSort('name')} style={thStyle('left')}>
              Название товара{renderArrow('name')}
            </th>
            <th onClick={() => handleSort('price')} style={thStyle('right')}>
              Цена{renderArrow('price')}
            </th>
            <th onClick={() => handleSort('discounted_price')} style={thStyle('right')}>
              Цена со скидкой{renderArrow('discounted_price')}
            </th>
            <th onClick={() => handleSort('rating')} style={thStyle('center')}>
              Рейтинг{renderArrow('rating')}
            </th>
            <th onClick={() => handleSort('review_count')} style={thStyle('right')}>
              Количество отзывов{renderArrow('review_count')}
            </th>
          </tr>
        </thead>
        <tbody>
          {products.length === 0 ? (
            <tr>
              <td colSpan="5" style={emptyCellStyle}>
                Нет товаров для отображения
              </td>
            </tr>
          ) : (
            products.map((product, i) => (
              <tr key={product.id || i} style={{ backgroundColor: i % 2 === 0 ? '#fff' : '#f9f9f9' }}>
                <td style={{ ...tdStyle, maxWidth: '300px', wordWrap: 'break-word' }}>
                  {product.name || 'Без названия'}
                </td>
                <td style={{ ...tdStyle, textAlign: 'right' }}>{formatPrice(product.price)}</td>
                <td style={{ ...tdStyle, textAlign: 'right' }}>{formatPrice(product.discounted_price)}</td>
                <td style={{ ...tdStyle, textAlign: 'center' }}>{formatRating(product.rating)}</td>
                <td style={{ ...tdStyle, textAlign: 'right' }}>{formatReviewCount(product.review_count)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

// Стили
const thStyle = (align = 'left') => ({
  padding: '12px 8px',
  cursor: 'pointer',
  border: '1px solid #ddd',
  textAlign: align,
  userSelect: 'none',
});

const tdStyle = {
  padding: '8px',
  border: '1px solid #ddd',
};

const emptyCellStyle = {
  padding: '20px',
  textAlign: 'center',
  border: '1px solid #ddd',
  fontStyle: 'italic',
  color: '#666',
};

export default ProductTable;
