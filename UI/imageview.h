#ifndef IMAGEVIEW_H
#define IMAGEVIEW_H

#include <QWidget>
#include <QString>

class imageView : public QWidget
{
    Q_OBJECT
public:
    explicit imageView(QWidget *parent = 0);
    explicit imageView(QString *s,QWidget *parent=0);
    
signals:
    
public slots:
    
};

#endif // IMAGEVIEW_H
