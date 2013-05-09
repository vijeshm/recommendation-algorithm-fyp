#ifndef IMAGE_H
#define IMAGE_H

#include <QWidget>

namespace Ui {
class Image;
}

class Image : public QWidget
{
    Q_OBJECT
    
public:
    explicit Image(QWidget *parent = 0);
    explicit Image(QString s,QWidget *parent=0);
    ~Image();
    
private:
    Ui::Image *ui;
};

#endif // IMAGE_H
